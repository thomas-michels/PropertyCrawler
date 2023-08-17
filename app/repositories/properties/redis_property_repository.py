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

    def insert_simple_properties(self, properties: List[SimpleProperty]) -> bool:
        try:
            properties_ids = {}
            timed_cache = 60 * _env.TIMED_CACHE

            for property in properties:
                properties_ids[property.id] = property.id

                self.__redis_connection.conn.set(f"property:{property.id}", property.model_dump_json(), ex=timed_cache)

            self.__redis_connection.conn.zadd("properties", properties_ids)
            self.__redis_connection.conn.expire("properties", timed_cache)

        except Exception as error:
            _logger.error(f"Error on redis update_data: {str(error)}")
            return False

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
