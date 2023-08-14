from app.repositories.properties.property_repository import PropertyRepository
from app.repositories.property_history.property_history_repository import PropertyHistoryRepository
from app.repositories.modalities.modality_repository import ModalityRepository
from app.repositories.neighborhoods.neighborhood_repository import NeighborhoodRepository
from app.repositories.streets.street_repository import StreetRepository
from app.repositories.companies.company_repository import CompanyRepository
from app.services.property_service import PropertyService
from app.db.base_connection import DBConnection


def property_composer(connection: DBConnection) -> PropertyService:
    service = PropertyService(
        property_repository=PropertyRepository(connection=connection),
        property_history_repository=PropertyHistoryRepository(connection=connection),
        modality_repository=ModalityRepository(connection=connection),
        neighborhood_repository=NeighborhoodRepository(connection=connection),
        street_repository=StreetRepository(connection=connection),
        company_repository=CompanyRepository(connection=connection)
    )
    return service
