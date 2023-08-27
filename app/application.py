from app.configs import get_logger
from app.db import start_pool, close_pool
from app.dependencies.worker import (
    KombuWorker,
    RegisterQueues,
    start_connection_bus
)
# from app.composers import property_composer
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

            # self.__start_cache()

            _logger.info("Starting Worker")

            with start_connection_bus() as conn:
                worker = KombuWorker(conn, queues, self.pool)
                worker.run()

        except KeyboardInterrupt:
            _logger.info("Stopping Worker")
            close_pool(self.pool)
            quit()

    def terminate(self, *args):
        close_pool(self.pool)
        quit()

    # def __start_cache(self):
    #     _logger.info("Fetching all properties had inserted")
    #     with RawPGConnection() as pg_connection:
    #         redis_connection = RedisClient()

    #         property_services = property_composer(
    #             connection=pg_connection,
    #             redis_connection=redis_connection
    #         )

    #         if not property_services.check_if_cache_is_udpated():
    #             property_services.updating_cache()
    #             all_properties = property_services.search_all_codes(active=True)

    #             for simple_property in all_properties:
    #                 property_services.save_on_cache(simple_property=simple_property)

    #         redis_connection.close()

    #     _logger.info("Properties cached")
