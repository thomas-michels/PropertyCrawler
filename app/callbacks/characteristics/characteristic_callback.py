from crawler.portal_imoveis.characteristics_crawler import start_characteristics_crawler
from app.callbacks.callback_interface.callback_base import Callback
from app.db import DBConnection
from app.dependencies import RedisClient
from app.dependencies.worker.utils.event_schema import EventSchema
from app.dependencies.worker import KombuProducer
from app.configs import get_environment, get_logger
from time import sleep
from datetime import datetime
from random import randint

_env = get_environment()
_logger = get_logger(__name__)


class CharacteristicCallback(Callback):

    def __init__(self, conn: DBConnection, redis_conn: RedisClient) -> None:
        super().__init__(conn, redis_conn)

    def handle(self, message: EventSchema) -> bool:

        sleep(randint(5, 15))
        
        company = message.payload["company"]

        if company == "portal_imoveis":
            _logger.info(f"Starting Portal imoveis characteristics crawler")
            raw_property = start_characteristics_crawler(message=message)

        else:
            return False

        if raw_property:
            new_message = EventSchema(
                id=message.id,
                origin=message.sent_to,
                sent_to=_env.PROPERTY_VALIDATOR_CHANNEL,
                payload=raw_property.model_dump(),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            KombuProducer.send_messages(conn=self.conn, message=new_message)

            return True
