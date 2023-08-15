from app.callbacks.callback_interface.callback_base import Callback
from app.db import DBConnection
from app.dependencies.worker import EventSchema, KombuProducer
from app.composers import property_composer
from app.configs import get_environment, get_logger
import requests
from requests.exceptions import HTTPError

_env = get_environment()
_logger = get_logger()


class PropertyInCallback(Callback):

    def __init__(self, conn: DBConnection) -> None:
        super().__init__(conn)
        self.__property_services = property_composer(connection=self.conn)

    def handle(self, message: EventSchema) -> bool:
        
        property_url = message.payload.get("property_url")

        if not property_url:
            return True
        
        response = requests.get(url=property_url)

        try:
            response.raise_for_status()

            new_message = EventSchema(
                sent_to=_env.CHARACTERISTICS_CHANNEL,
                payload=message.payload
            )

            return KombuProducer.send_messages(message=new_message)

        except HTTPError:
            code = message.payload["code"]
            company = message.payload["company"]
        
            property_in_db = self.__property_services.search_by_code_and_company(code=code, company=company)

            if property_in_db:
                self.__property_services.delete(id=property_in_db.id)
                _logger.warning(f"Property deleted with id={property_in_db.id}")

            return True
