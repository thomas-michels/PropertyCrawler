from app.callbacks.callback_interface.callback_base import Callback
from app.db import DBConnection
from app.dependencies import RedisClient
from app.entities import RawProperty
from app.dependencies.worker.utils.event_schema import EventSchema
from app.dependencies.worker import KombuProducer
from app.composers import property_composer
from app.configs import get_logger, get_environment
from datetime import datetime

_logger = get_logger(__name__)
_env = get_environment()


class UpdatePropertyCallback(Callback):

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

            is_updated = self.__property_services.update_price(
                property=property_in_db,
                new_price=raw_property.price
            )

            if is_updated:
                _logger.info(f"Property with id {property_in_db.id} has a new price!")
                new_message = EventSchema(
                    id=message.id,
                    origin=message.sent_to,
                    sent_to=_env.PROPERTY_OUT_CHANNEL,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                KombuProducer.send_messages(conn=self.conn, message=new_message)

            return is_updated

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {message.model_dump_json()}")
            return False
