from app.callbacks.callback_interface.callback_base import Callback
from app.db import DBConnection
from app.dependencies.worker import EventSchema


class NewAddressCallback(Callback):

    def __init__(self, conn: DBConnection) -> None:
        super().__init__(conn)

    def handle(self, message: EventSchema) -> bool:
        return super().handle(message)
