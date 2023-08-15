from abc import ABC, abstractclassmethod


class PropertyCrawler(ABC):

    @abstractclassmethod
    def extract_urls(cls):
        ...
