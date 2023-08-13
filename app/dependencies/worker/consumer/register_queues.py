"""
    Module for register queues
"""
from .manager import QueueManager
from app.configs import get_logger, get_environment
from app.callbacks.properties import (
    PropertyInCallback,
    SavePropertyCallback,
    UpdatePropertyCallback,
    InactivePropertyCallback
)


_logger = get_logger(name=__name__)
_env = get_environment()


class RegisterQueues:
    """
    RegisterQueues class
    """

    @staticmethod
    def register() -> QueueManager:
        _logger.info("Starting QueueManager")
        queue_manager = QueueManager()

        queue_manager.register_callback(
            _env.PROPERTY_IN_CHANNEL, PropertyInCallback
        )

        queue_manager.register_callback(
            _env.SAVE_PROPERTY_CHANNEL, SavePropertyCallback
        )

        queue_manager.register_callback(
            _env.UPDATE_PROPERTY_CHANNEL, UpdatePropertyCallback
        )

        queue_manager.register_callback(
            _env.INACTIVE_PROPERTY_CHANNEL, InactivePropertyCallback
        )

        _logger.info("All queues started")

        return queue_manager
