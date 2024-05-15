from pydantic import BaseModel, ValidationError


class Address(BaseModel):
    name: str
    latitude: float
    longitude: float





