from app.callbacks.callback_interface.callback_base import Callback
from app.db import DBConnection
from app.dependencies import RedisClient
from app.dependencies.worker.utils.event_schema import EventSchema
from app.dependencies.worker import KombuProducer
from app.configs import get_environment, get_logger
from app.composers import property_composer
import requests
from requests.exceptions import HTTPError
from datetime import datetime
from time import sleep
from random import randint

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
        
        property_url = message.payload.get("property_url")

        if not property_url:
            return True

        simple_property = self.__property_services.search_by_url(url=property_url)

        if simple_property:
            _logger.info(f"Property had already saved today - URL: {property_url}")
            new_message = EventSchema(
                id=message.id,
                origin=message.sent_to,
                sent_to=_env.PROPERTY_OUT_CHANNEL,
                payload={},
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            return KombuProducer.send_messages(conn=self.conn, message=new_message)

        if message.payload["company"] == "zap_imoveis":
            headers = {
                "domain": ".zapimoveis.com.br",
                "X-Domain": ".zapimoveis.com.br",
                "Cookie": "__cfruid=72ab1a4d676a1b254f1c31fcdceee752d70655ef-1692746103",
                "User-Agent": "PostmanRuntime/7.32.3"
            }
            sleep(randint(5, 15))
            response = requests.get(url=property_url, headers=headers)

        else:
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
