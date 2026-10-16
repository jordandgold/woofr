from datetime import datetime, timezone
from typing import Literal

from pydantic import NaiveDatetime, field_serializer
from sqlmodel import Field, SQLModel


def utcnow() -> datetime:
    """Naive UTC timestamp (SQLite doesn't store timezones)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


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
    created_at: NaiveDatetime = Field(default_factory=utcnow)

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        # Stored as naive UTC; send an explicit UTC marker so browsers parse it correctly.
        return value.isoformat() + "Z"

class ProfileCreate(SQLModel):
    name: str
    breed: str
    age: int
    distanceMiles: float
    available: bool
    energyLevel: str
    bio: str



class ProfileCreate(SQLModel):
    """Client-supplied fields; id, favorited and imageUrl are set by the server."""

    name: str = Field(min_length=1, max_length=40)
    breed: str = Field(min_length=1, max_length=60)
    age: int = Field(ge=0, le=30)
    distanceMiles: float = Field(ge=0)
    available: bool
    energyLevel: Literal["low", "medium", "high"]
    bio: str = Field(min_length=1, max_length=200)
