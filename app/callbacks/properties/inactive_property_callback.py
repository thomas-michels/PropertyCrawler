from app.callbacks.callback_interface.callback_base import Callback
from app.db import DBConnection
from app.dependencies.worker import EventSchema
from app.composers import property_composer
from app.configs import get_logger, get_environment
from app.dependencies.worker import KombuProducer, EventSchema

_logger = get_logger(__name__)
_env = get_environment()


class InactivePropertyCallback(Callback):

    def __init__(self, conn: DBConnection) -> None:
        super().__init__(conn)
        self.__property_services = property_composer(connection=self.conn)

    def handle(self, message: EventSchema) -> bool:
        code = message.payload["code"]
        company = message.payload["company"]
    
        property_in_db = self.__property_services.search_by_code_and_company(code=code, company=company)

        if property_in_db:
            self.__property_services.delete(id=property_in_db.id)
            _logger.info(f"Property deleted with id={property_in_db.id}")

        new_message = EventSchema(
            id=message.id,
            origin=message.sent_to,
            sent_to=_env.PROPERTY_OUT_CHANNEL
        )

        KombuProducer.send_messages(conn=self.conn, message=new_message)

        return True
