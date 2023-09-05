from app.callbacks.callback_interface.callback_base import Callback
from app.db import DBConnection
from app.dependencies import RedisClient
from app.entities import RawProperty
from app.dependencies.worker.utils.event_schema import EventSchema
from app.dependencies.worker import KombuProducer
from app.composers import property_composer
from app.configs import get_environment, get_logger
from datetime import datetime

_env = get_environment()
_logger = get_logger(__name__)


class PropertyValidatorCallback(Callback):

    def __init__(self, conn: DBConnection, redis_conn: RedisClient) -> None:
        super().__init__(conn, redis_conn)
        self.__property_services = property_composer(connection=self.conn, redis_connection=self.redis_conn)

    def handle(self, message: EventSchema) -> bool:
        try:
            raw_property = RawProperty(**message.payload)

            property_in_db = self.__property_services.search_by_code_and_company(
                code=raw_property.code,
                company=raw_property.company
            )

            if property_in_db.price != raw_property.price:
                new_message = EventSchema(
                    id=message.id,
                    origin=message.sent_to,
                    sent_to=_env.UPDATE_PROPERTY_CHANNEL,
                    payload=raw_property.model_dump_json(),
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                return KombuProducer.send_messages(conn=self.conn, message=new_message)

            else:
                new_message = EventSchema(
                    id=message.id,
                    origin=message.sent_to,
                    sent_to=_env.PROPERTY_OUT_CHANNEL,
                    payload={},
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                return KombuProducer.send_messages(conn=self.conn, message=new_message)

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {message.model_dump_json()}")
            return False
