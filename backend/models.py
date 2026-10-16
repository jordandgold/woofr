from pydantic import BaseModel


class Profile(BaseModel):
    id: str
    name: str
    breed: str
    age: int
    distanceMiles: float
    available: bool
    energyLevel: str
    bio: str
    imageUrl: str
