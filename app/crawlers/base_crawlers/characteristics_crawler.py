from abc import ABC, abstractclassmethod


class CharacteristicsCrawler(ABC):

    @abstractclassmethod
    def extract_characteristics(cls):
        ...
