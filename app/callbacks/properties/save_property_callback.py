from app.callbacks.callback_interface.callback_base import Callback
from app.db import DBConnection
from app.dependencies import RedisClient
from app.entities import RawProperty
from app.composers import property_composer
from app.dependencies.worker.utils.event_schema import EventSchema
from app.dependencies.worker import KombuProducer
from app.configs import get_environment, get_logger
from datetime import datetime

_env = get_environment()
_logger = get_logger(__name__)


class SavePropertyCallback(Callback):

    def __init__(self, conn: DBConnection, redis_conn: RedisClient) -> None:
        super().__init__(conn, redis_conn)
        self.__property_services = property_composer(connection=self.conn, redis_connection=self.redis_conn)

    def handle(self, message: EventSchema) -> bool:
        try:
            raw_property = RawProperty(**message.payload)
            
            property_in_db = self.__property_services.create(raw_property=raw_property)

            if property_in_db:
                new_message = EventSchema(
                    id=message.id,
                    origin=message.sent_to,
                    sent_to=_env.PROPERTY_OUT_CHANNEL,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                KombuProducer.send_messages(conn=self.conn, message=new_message)

                return True

        except Exception as error:
            _logger.error(f"Error: {error}. Data: {message.model_dump_json()}")
