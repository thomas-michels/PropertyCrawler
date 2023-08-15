from app.crawlers.base_crawlers import PropertyCrawler
from app.configs import get_logger, get_environment

_logger = get_logger(__name__)
_env = get_environment()


class PortalImoveisCrawler(PropertyCrawler):

    def extract_urls(cls):
        _logger.info("Portal Imoveis Crawler starting")
