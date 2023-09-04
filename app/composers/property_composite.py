from app.repositories.properties.property_repository import PropertyRepository
from app.repositories.properties.redis_property_repository import RedisPropertyRepository
from app.repositories.property_history.property_history_repository import PropertyHistoryRepository
from app.repositories.modalities.modality_repository import ModalityRepository
from app.repositories.companies.company_repository import CompanyRepository
from app.services.property_service import PropertyService
from app.db.base_connection import DBConnection
from app.dependencies import RedisClient


def property_composer(connection: DBConnection, redis_connection: RedisClient) -> PropertyService:
    service = PropertyService(
        property_repository=PropertyRepository(connection=connection),
        redis_property_repository=RedisPropertyRepository(redis_connection=redis_connection),
        property_history_repository=PropertyHistoryRepository(connection=connection),
        modality_repository=ModalityRepository(connection=connection),
        company_repository=CompanyRepository(connection=connection)
    )
    return service
