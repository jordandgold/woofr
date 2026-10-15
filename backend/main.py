from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Woofr API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Profile(BaseModel):
    id: str
    name: str
    breed: str
    age: int
    distanceMiles: float
    available: bool
    energyLevel: str
    bio: str


profiles = [
    Profile(
        id="1",
        name="Biscuit",
        breed="Golden Retriever",
        age=3,
        distanceMiles=0.4,
        available=True,
        energyLevel="high",
        bio="Professional tennis ball enthusiast. Will trade friendship for treats.",
    ),
    Profile(
        id="2",
        name="Frank",
        breed="French Bulldog",
        age=5,
        distanceMiles=1.2,
        available=False,
        energyLevel="low",
        bio="Neighborhood nap champion. Selectively social.",
    ),
    Profile(
        id="3",
        name="Luna",
        breed="Corgi",
        age=2,
        distanceMiles=0.8,
        available=True,
        energyLevel="high",
        bio="Short legs, big personality. Seeking zoomie partners.",
    ),
    Profile(
        id="4",
        name="Mochi",
        breed="Shiba Inu",
        age=4,
        distanceMiles=2.1,
        available=True,
        energyLevel="medium",
        bio="Independent queen. Must pass the vibe check.",
    ),
    Profile(
        id="5",
        name="Teddy",
        breed="Labrador",
        age=1,
        distanceMiles=0.6,
        available=False,
        energyLevel="high",
        bio="Still learning that other dogs' tennis balls aren't mine.",
    ),
]

# Return all profiles when no filters are supplied.
# Match search against name or breed, ignoring case.
# Return only available profiles when availableOnly=true.
# Apply both conditions when both parameters are supplied.
# Return an empty array [] when no profiles match.

@app.get("/api/profiles", response_model=list[Profile])
def get_profiles(
        search: str | None = None,
        availableOnly: bool = False,
    ):

    filtered_profiles = profiles

    if availableOnly:
        filtered_profiles = [p for p in filtered_profiles if p.available]

    if search:
        search_lower = search.lower()
        filtered_profiles = [
            p for p in filtered_profiles
            if search_lower in p.name.casefold() or search_lower in p.breed.casefold()
        ]

    return filtered_profiles