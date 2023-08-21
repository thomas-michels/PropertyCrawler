from app.configs import get_logger
from app.db import start_pool, close_pool
from app.dependencies.worker import (
    KombuWorker,
    RegisterQueues,
    start_connection_bus
)
import signal

_logger = get_logger(__name__)


class Application:

    def __init__(self) -> None:
        signal.signal(signal.SIGTERM, self.terminate)
        signal.signal(signal.SIGINT, self.terminate)

    def start(self):
        try:
            self.pool = start_pool()

            queues = RegisterQueues.register()

            _logger.info("Starting Crawlers")

            with start_connection_bus() as conn:
                worker = KombuWorker(conn, queues, self.pool)
                worker.run()

        except KeyboardInterrupt:
            _logger.info("Stopping Crawlers")
            close_pool(self.pool)
            quit()

    def terminate(self, *args):
        close_pool(self.pool)
        quit()
