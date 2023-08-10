from app.configs import get_logger

_logger = get_logger(__name__)


class Application:

    @classmethod
    def start(cls):
        try:
            _logger.info("Starting Crawlers")

        except KeyboardInterrupt:
            _logger.info("Stopping Crawlers")
