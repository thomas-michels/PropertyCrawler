from app.repositories.properties import PropertyRepository, RedisPropertyRepository
from app.repositories.property_history import PropertyHistoryRepository
from app.repositories.modalities import ModalityRepository
from app.repositories.neighborhoods import NeighborhoodRepository
from app.repositories.streets import StreetRepository
from app.repositories.companies import CompanyRepository
from app.entities import (
    Property,
    PropertyInDB,
    SimpleProperty,
    RawProperty,
    PropertyHistory
)
from typing import List


class PropertyService:

    def __init__(
            self,
            property_repository: PropertyRepository,
            redis_property_repository: RedisPropertyRepository,
            property_history_repository: PropertyHistoryRepository,
            modality_repository: ModalityRepository,
            neighborhood_repository: NeighborhoodRepository,
            street_repository: StreetRepository,
            company_repository: CompanyRepository,
        ) -> None:
        self.__property_repository = property_repository
        self.__redis_property_repository = redis_property_repository
        self.__property_history_repository = property_history_repository
        self.__modality_repository = modality_repository
        self.__neighborhood_repository = neighborhood_repository
        self.__street_repository = street_repository
        self.__company_repository = company_repository

    def create(self, raw_property: RawProperty) -> PropertyInDB:
        property = Property(
            code=raw_property.code,
            title=raw_property.title,
            price=raw_property.price,
            description=raw_property.description,
            rooms=raw_property.rooms,
            bathrooms=raw_property.bathrooms,
            size=raw_property.size,
            parking_space=raw_property.parking_space,
            image_url=raw_property.image_url,
            property_url=raw_property.property_url,
            type=raw_property.type,
            number=raw_property.number
        )

        modality_in_db = self.__modality_repository.select_by_name(name=raw_property.modality)

        if not modality_in_db and raw_property.modality:
            modality_in_db = self.__modality_repository.insert(name=raw_property.modality)

        neighborhood_in_db = self.__neighborhood_repository.select_by_name(name=raw_property.neighborhood)

        if not neighborhood_in_db and raw_property.neighborhood:
            neighborhood_in_db = self.__neighborhood_repository.insert(name=raw_property.neighborhood)

        street_in_db = self.__street_repository.select_by_name(name=raw_property.street)

        if not street_in_db and raw_property.street:
            street_in_db = self.__street_repository.insert(neighborhood_id=neighborhood_in_db.id, name=raw_property.street)

        company_in_db = self.__company_repository.select_by_name(name=raw_property.company)

        property.modality_id = modality_in_db.id if modality_in_db else None
        property.neighborhood_id = neighborhood_in_db.id if neighborhood_in_db else None
        property.street_id = street_in_db.id if street_in_db else None
        property.company_id = company_in_db.id if company_in_db else None

        property_in_db = self.__property_repository.insert(property=property)

        if property_in_db:
            self.__property_repository.conn.commit()

            simple = SimpleProperty(
                id=property_in_db.id,
                code=property_in_db.code,
                company_id=property_in_db.company_id,
                property_url=property_in_db.property_url
            )

            self.__redis_property_repository.insert_simple_property(property=simple)

            return property_in_db

    def search_all_codes(self, active: bool = False) -> List[SimpleProperty]:
        return self.__property_repository.select_all_codes(active=active)
    
    def search_by_url(self, url: str) -> SimpleProperty:
        return self.__redis_property_repository.select_by_url(url=url)

    def search_by_id(self, id: int) -> PropertyInDB:
        return self.__property_repository.select_by_id(id=id)
    
    def search_by_code_and_company(self, code: int, company: str) -> PropertyInDB:
        company_in_db = self.__company_repository.select_by_name(name=company)
        if company_in_db:
            return self.__property_repository.select_by_code_and_company(code=code, company_id=company_in_db.id)

    def update_price(self, id: int, new_price: float) -> bool:
        property = self.__property_repository.select_by_id(id=id)

        if not property:
            return False

        is_updated = self.__property_repository.update_price(id=id, new_price=new_price)

        if is_updated:
            property_history = PropertyHistory(
                price=property.price,
                property_id=property.id
            )

            property_history_in_db = self.__property_history_repository.insert(property_history=property_history)

            return bool(property_history_in_db)
        
        self.__property_repository.conn.commit()

        return False

    def delete(self, id: int) -> bool:
        is_deleted = self.__property_repository.delete(id=id)
        self.__property_repository.conn.commit()
        return is_deleted
