"""
    Module for event schemas
"""
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic.types import UUID4
from uuid import uuid4


class EventSchema(BaseModel):
    """
    Event Schema
    """

    id: UUID4 = Field(default=str(uuid4()), example="16f8ddc6-3697-4b90-a5c5-1b60e26de6dc")
    sended_to: str = Field(example="Queue")
    payload: dict = Field()
    creation_date: datetime = Field(default=datetime.now(), example="2022-06-04 22:13:19.332981")
