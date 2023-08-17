from app.callbacks.callback_interface.callback_base import Callback
from app.db import DBConnection
from app.dependencies import RedisClient
from app.entities import RawProperty
from app.composers import property_composer
from app.dependencies.worker.utils.event_schema import EventSchema
from app.dependencies.worker import KombuProducer
from app.configs import get_environment

_env = get_environment()


class SavePropertyCallback(Callback):

    def __init__(self, conn: DBConnection, redis_conn: RedisClient) -> None:
        super().__init__(conn, redis_conn)
        self.__property_services = property_composer(connection=self.conn, redis_connection=self.redis_conn)

    def handle(self, message: EventSchema) -> bool:
        raw_property = RawProperty(**message.payload)
        
        property_in_db = self.__property_services.create(raw_property=raw_property)

        if property_in_db:
            new_message = EventSchema(
                id=message.id,
                origin=message.sent_to,
                sent_to=_env.PROPERTY_OUT_CHANNEL
            )
            KombuProducer.send_messages(conn=self.conn, message=new_message)

            return True
