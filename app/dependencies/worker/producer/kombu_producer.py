"""
    Module for Kombu Producer class
"""

from kombu.mixins import Producer
from app.dependencies.worker.utils import start_connection_bus, connect_on_exchange, EventSchema
from app.configs import get_logger, get_environment

_env = get_environment()
_logger = get_logger(name=__name__)


class KombuProducer:
    """
    Class for Producer to send messages in queues
    """

    @staticmethod
    def send_messages(message: EventSchema) -> bool:
        """
        Method to send messages

        :param message: EventSchema

        :return: bool
        """
        try:
            with start_connection_bus() as conn:
                producer = Producer(conn)
                producer.publish(
                    body=message.model_dump(),
                    exchange=connect_on_exchange(_env.RBMQ_EXCHANGE),
                    routing_key=message.sent_to,
                )

            _logger.info(f"Sent message to {message.sent_to}")
            return True

        except Exception as error:
            _logger.error(
                f"Error on send message to {message.sent_to}. Error: {error}"
            )
