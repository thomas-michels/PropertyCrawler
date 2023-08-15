from app.callbacks.callback_interface.callback_base import Callback
from app.db import DBConnection
from app.entities import RawProperty
from app.dependencies.worker.utils.event_schema import EventSchema
from app.dependencies.worker import KombuProducer
from app.composers import property_composer
from app.configs import get_environment, get_logger

_env = get_environment()
_logger = get_logger(__name__)


class PropertyValidatorCallback(Callback):

    def __init__(self, conn: DBConnection) -> None:
        super().__init__(conn)
        self.__property_services = property_composer(connection=self.conn)

    def handle(self, message: EventSchema) -> bool:
        try:
            raw_property = RawProperty(**message.payload)

            property_in_db = self.__property_services.search_by_code_and_company(
                code=raw_property.code,
                company=raw_property.company
            )

            if not property_in_db:
                new_message = EventSchema(
                    id=message.id,
                    origin=message.sent_to,
                    sent_to=_env.SAVE_PROPERTY_CHANNEL,
                    payload=raw_property.model_dump()
                )
                return KombuProducer.send_messages(conn=self.conn, message=new_message)

            if property_in_db.price != raw_property.price:
                new_message = EventSchema(
                    id=message.id,
                    origin=message.sent_to,
                    sent_to=_env.UPDATE_PROPERTY_CHANNEL,
                    payload=raw_property.model_dump()
                )
                return KombuProducer.send_messages(conn=self.conn, message=new_message)

            return True

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {message.model_dump()}")
            return False
