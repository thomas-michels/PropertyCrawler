from app.callbacks.callback_interface.callback_base import Callback
from app.db import DBConnection
from app.dependencies import RedisClient
from app.dependencies.worker.utils.event_schema import EventSchema
from app.dependencies.worker import KombuProducer
from app.entities import RawProperty
from app.configs import get_environment, get_logger
from app.composers import property_composer
import requests
from requests.exceptions import HTTPError
from datetime import datetime

_env = get_environment()
_logger = get_logger(__name__)


class PropertyInCallback(Callback):

    def __init__(self, conn: DBConnection, redis_conn: RedisClient) -> None:
        super().__init__(conn, redis_conn)
        self.__property_services = property_composer(
            connection=self.conn,
            redis_connection=self.redis_conn
        )

    def handle(self, message: EventSchema) -> bool:
        try:
            property_url = message.payload.get("property_url")

            if not property_url:
                return True

            property = self.__property_services.search_by_url(url=property_url)

            if property:
                new_message = EventSchema(
                    id=message.id,
                    origin=message.sent_to,
                    sent_to=_env.PROPERTY_VALIDATOR_CHANNEL,
                    payload=message.payload,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                return KombuProducer.send_messages(conn=self.conn, message=new_message)            

            raw_property = RawProperty(**message.payload)
            address = None

            if raw_property.zip_code:
                try:
                    if raw_property.zip_code[-3] != "-":
                        zip_code = raw_property.zip_code.split()
                        zip_code.insert(-3, "-")
                        raw_property.zip_code = "".join(zip_code)

                    url = f"{_env.BASE_ADDRESS_URL}/address/zip-code/{raw_property.zip_code}"

                    address = requests.get(url=url)
                    address.raise_for_status()
                    address = address.json()

                except HTTPError:
                    ...

            if raw_property.street and not address:
                try:
                    url = f"{_env.BASE_ADDRESS_URL}/address/street/{raw_property.street}"

                    address = requests.get(url=url)
                    address.raise_for_status()
                    address = address.json()

                except HTTPError:
                    ...

            if raw_property.neighborhood and not address:
                try:
                    url = f"{_env.BASE_ADDRESS_URL}/address/neighborhood/{raw_property.neighborhood}"

                    address = requests.get(url=url)
                    address.raise_for_status()
                    address = address.json()

                except HTTPError:
                    ...

            if address:
                raw_property.street_id = address["street_id"]
                raw_property.street = address["street_name"]
                raw_property.neighborhood_id = address["neighborhood_id"]
                raw_property.neighborhood = address["neighborhood_name"]

            new_message = EventSchema(
                id=message.id,
                origin=message.sent_to,
                sent_to=_env.SAVE_PROPERTY_CHANNEL,
                payload=raw_property.model_dump(),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            return KombuProducer.send_messages(conn=self.conn, message=new_message)

        except Exception as error:
            _logger.error(f"Error: {str(error)}")
            return True
