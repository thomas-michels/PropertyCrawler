"""
Kombu worker class module
"""

from psycopg_pool import ConnectionPool
from app.db import PGConnection
from kombu import Connection
from kombu.mixins import ConsumerMixin
from app.configs import get_logger
from app.exceptions import QueueNotFound
from app.dependencies.worker.consumer.manager import QueueManager
from app.dependencies.worker.utils.validate_event import payload_conversor
from app.dependencies.redis_client import RedisClient

_logger = get_logger(name=__name__)


class KombuWorker(ConsumerMixin):
    """
    This class is Kombu Worker
    """

    def __init__(self, connection: Connection, queues: QueueManager, pool: ConnectionPool):
        self.queues = queues
        self.connection = connection
        self.pool = pool

    def get_consumers(self, consumer, channel):
        return [
            consumer(queues=self.queues.get_queues(), callbacks=[self.process_task])
        ]

    def process_task(self, body, message):
        try:
            infos = message.delivery_info
            _logger.info(f"Message received at {infos['routing_key']}")
            callback = self.queues.get_function(infos["routing_key"])
            with RedisClient() as redis_conn:
                with self.pool.connection() as conn:
                    pg_connection = PGConnection(conn=conn)
                    callback = callback(pg_connection, redis_conn)
                    event_schema = payload_conversor(body)
                    if event_schema:
                        if callback.handle(event_schema):
                            message.ack()

        except QueueNotFound:
            _logger.error("Callback not found!")

        except Exception as error:
            _logger.error(f"Error on process_task - {error}")
