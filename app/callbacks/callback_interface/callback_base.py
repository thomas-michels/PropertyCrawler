"""
    Module for callbacks interface
"""

from abc import abstractmethod, ABC
from app.db import DBConnection
from app.dependencies.worker.utils.event_schema import EventSchema


class Callback(ABC):
    """
    Class for callback base
    """

    def __init__(self, conn: DBConnection) -> None:
        self.conn = conn

    @abstractmethod
    def handle(self, message: EventSchema) -> bool:
        """
        This method handle message and returns a bool

        :param:
            message
        :return: 
            Boolean
        """
