from pydantic import BaseModel, Field
from datetime import datetime
from .company import CompanyEnum


class RawProperty(BaseModel):
    code: int = Field(example=123)
    company: CompanyEnum = Field(example=CompanyEnum.PORTAL_IMOVEIS)
    title: str = Field(example="house")
    price: float = Field(example=123.3)
    description: str = Field(example="description")
    neighborhood: str = Field(example="Itoupava Central")
    rooms: int = Field(example=123)
    bathrooms: int = Field(example=123)
    size: float = Field(example=123)
    parking_space: int = Field(example=123)
    modality: str = Field(example="buy")
    property_url: str = Field(example="www.url.com")
    image_url: str = Field(example="www.url.com")
    type: str = Field(example="House")
    number: str = Field(example="123")
    street: str = Field(example="Rua Antonio da Veiga")


class Property(BaseModel):
    code: int = Field(example=123)
    company_id: int = Field(example=123)
    title: str = Field(example="house")
    price: float = Field(example=123.3)
    description: str = Field(example="description")
    neighborhood_id: int = Field(example=123)
    rooms: int = Field(example=123)
    bathrooms: int = Field(example=123)
    size: float = Field(example=123)
    parking_space: int = Field(example=123)
    modality_id: int = Field(example=123)
    image_url: str = Field(example="www.url.com")
    property_url: str = Field(example="www.url.com")
    type: str = Field(example="House")
    number: str = Field(example="123")
    street_id: int = Field(example=123)
    created_at: datetime = Field(example=str(datetime.now()), default=datetime.now())
    updated_at: datetime = Field(example=str(datetime.now()), default=datetime.now())


class PropertyInDB(Property):
    id: int = Field(example=123)
