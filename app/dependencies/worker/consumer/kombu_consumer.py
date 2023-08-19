"""
Kombu worker class module
"""

from psycopg_pool import ConnectionPool
from app.db import PGConnection
from kombu import Connection
from kombu.common import QoS
from kombu.mixins import ConsumerMixin
from app.configs import get_logger, get_environment
from app.exceptions import QueueNotFound
from app.dependencies.worker.consumer.manager import QueueManager
from app.dependencies.worker.utils.validate_event import payload_conversor
from app.dependencies.redis_client import RedisClient

_logger = get_logger(name=__name__)
_env = get_environment()


class KombuWorker(ConsumerMixin):
    """
    This class is Kombu Worker
    """

    def __init__(self, connection: Connection, queues: QueueManager, pool: ConnectionPool):
        self.queues = queues
        self.connection = connection
        self.pool = pool
        self.qos = QoS(self.connection, initial_value=_env.PREFETCH_VALUE)

    def get_consumers(self, consumer, channel):
        return [
            consumer(queues=self.queues.get_queues(), callbacks=[self.process_task], prefetch_count=0)
        ]

    def process_task(self, body, message):
        try:
            self.qos.increment_eventually()
            infos = message.delivery_info
            _logger.info(f"Message received at {infos['routing_key']}")
            callback = self.queues.get_function(infos["routing_key"])
            redis_conn = RedisClient()
            with self.pool.connection() as conn:
                pg_connection = PGConnection(conn=conn)
                callback = callback(pg_connection, redis_conn)
                event_schema = payload_conversor(body)
                if event_schema:
                    if callback.handle(event_schema):
                        message.ack()
            
            redis_conn.close()
            self.qos.decrement_eventually()
            _logger.info(f"Message consumed at {event_schema.id}")

        except QueueNotFound:
            _logger.error("Callback not found!")

        except Exception as error:
            _logger.error(f"Error on process_task - {error}")
