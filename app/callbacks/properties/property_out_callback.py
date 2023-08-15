from app.callbacks.callback_interface.callback_base import Callback
from app.db import DBConnection
from app.dependencies.worker import EventSchema
from app.configs import get_logger

_logger = get_logger(__name__)


class PropertyOutCallback(Callback):

    def __init__(self, conn: DBConnection) -> None:
        super().__init__(conn)

    def handle(self, message: EventSchema) -> bool:
        _logger.info(f"Property flow completed.")
        return True
