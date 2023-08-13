from pydantic import BaseModel, Field


class Street(BaseModel):

    id: int = Field(example=123)
    name: str = Field(example="Antonio da Veiga")
