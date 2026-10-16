from sqlmodel import Field, SQLModel


class Profile(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    breed: str
    age: int
    distanceMiles: float
    available: bool
    energyLevel: str
    bio: str
    imageUrl: str
    favorited: bool = False
