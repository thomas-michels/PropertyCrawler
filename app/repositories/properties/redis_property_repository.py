from app.dependencies import RedisClient
from app.entities import SimpleProperty
from app.configs import get_environment, get_logger
from typing import List
import json

_env = get_environment()
_logger = get_logger(__name__)


class RedisPropertyRepository:

    def __init__(self, redis_connection: RedisClient) -> None:
        self.__redis_connection = redis_connection

    def insert_simple_property(self, property: SimpleProperty) -> bool:
        try:
            timed_cache = 60 * _env.TIMED_CACHE

            self.__redis_connection.conn.set(f"property:{property.id}", property.model_dump_json(), ex=timed_cache)
            self.__redis_connection.conn.set(f"property:{property.property_url}", property.model_dump_json(), ex=timed_cache)

            _logger.info(f"PropertyCached: {property.property_url}")
            return True

        except Exception as error:
            _logger.error(f"Error: {str(error)}")
            return False
        
    def is_updated(self) -> bool:
        return self.__redis_connection.conn.get(f"properties_updated")

    def updating(self) -> bool:
        timed_cache = 60 * _env.TIMED_CACHE
        return self.__redis_connection.conn.set(f"properties_updated", 1, ex=timed_cache)

    def select_by_url(self, url: str) -> SimpleProperty:
        try:
            raw_property = self.__redis_connection.conn.get(f"property:{url}")
            if raw_property:
                raw_property = json.loads()
                return SimpleProperty(**raw_property)

        except Exception as error:
            _logger.error(f"Error: {str(error)}")

    def select_all(self) -> List[SimpleProperty]:
        try:
            properties_ids = self.__redis_connection.conn.get("properties")
            properties = []

            if properties_ids:
                for property_id in properties_ids:
                    raw_property = self.__redis_connection.conn.get(f"property:{property_id}")
                    if raw_property:
                        raw_property = json.loads()
                        properties.append(SimpleProperty(**raw_property))

            return properties
        
        except Exception as error:
            _logger.error(f"Error: {error}")
            return []
