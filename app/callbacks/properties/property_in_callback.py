from app.callbacks.callback_interface.callback_base import Callback
from app.db import DBConnection
from app.dependencies import RedisClient
from app.dependencies.worker.utils.event_schema import EventSchema
from app.dependencies.worker import KombuProducer
from app.configs import get_environment
from app.composers import property_composer
import requests
from requests.exceptions import HTTPError
from datetime import datetime

_env = get_environment()


class PropertyInCallback(Callback):

    def __init__(self, conn: DBConnection, redis_conn: RedisClient) -> None:
        super().__init__(conn, redis_conn)
        self.__property_services = property_composer(
            connection=self.conn,
            redis_connection=self.redis_conn
        )

    def handle(self, message: EventSchema) -> bool:
        
        property_url = message.payload.get("property_url")

        if not property_url:
            return True

        simple_property = self.__property_services.search_by_url(url=property_url)

        if simple_property:
            return True

        response = requests.get(url=property_url)

        try:
            response.raise_for_status()

            new_message = EventSchema(
                id=message.id,
                origin=message.sent_to,
                sent_to=_env.CHARACTERISTICS_CHANNEL,
                payload=message.payload,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            return KombuProducer.send_messages(conn=self.conn, message=new_message)

        except HTTPError:
            new_message = EventSchema(
                id=message.id,
                origin=message.sent_to,
                sent_to=_env.INACTIVE_PROPERTY_CHANNEL,
                payload=message.payload,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            return True
