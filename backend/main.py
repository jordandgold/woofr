from pathlib import Path
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="Woofr API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Served under /api so the Vite dev proxy forwards image requests too.
app.mount(
    "/api/static",
    StaticFiles(directory=Path(__file__).parent / "static"),
    name="static",
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
    imageUrl: str


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
        imageUrl="/api/static/dogs/biscuit.jpg",
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
        imageUrl="/api/static/dogs/frank.jpg",
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
        imageUrl="/api/static/dogs/luna.jpg",
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
        imageUrl="/api/static/dogs/mochi.jpg",
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
        imageUrl="/api/static/dogs/teddy.jpg",
    ),
    Profile(
        id="6",
        name="Pepper",
        breed="Border Collie",
        age=3,
        distanceMiles=1.5,
        available=True,
        energyLevel="high",
        bio="Herds her humans to the dog park. Has opinions about squirrels.",
        imageUrl="/api/static/dogs/pepper.jpg",
    ),
    Profile(
        id="7",
        name="Waffles",
        breed="Dachshund",
        age=6,
        distanceMiles=0.9,
        available=False,
        energyLevel="low",
        bio="Long dog, short patience for stairs. Loves a good blanket burrito.",
        imageUrl="/api/static/dogs/waffles.jpg",
    ),
    Profile(
        id="8",
        name="Juniper",
        breed="Australian Shepherd",
        age=2,
        distanceMiles=2.4,
        available=True,
        energyLevel="high",
        bio="Frisbee prodigy. Will happily run until the sun goes down.",
        imageUrl="/api/static/dogs/juniper.jpg",
    ),
    Profile(
        id="9",
        name="Bruno",
        breed="Bernese Mountain Dog",
        age=4,
        distanceMiles=3.0,
        available=True,
        energyLevel="medium",
        bio="Gentle giant seeking shady spots and belly rubs.",
        imageUrl="/api/static/dogs/bruno.jpg",
    ),
    Profile(
        id="10",
        name="Olive",
        breed="Pug",
        age=7,
        distanceMiles=1.8,
        available=False,
        energyLevel="low",
        bio="Snores professionally. Available for snack-related negotiations.",
        imageUrl="/api/static/dogs/olive.jpg",
    ),
    Profile(
        id="11",
        name="Maple",
        breed="Beagle",
        age=5,
        distanceMiles=0.3,
        available=True,
        energyLevel="medium",
        bio="Nose-first explorer. If it smells interesting, she's already there.",
        imageUrl="/api/static/dogs/maple.jpg",
    ),
    Profile(
        id="12",
        name="Ziggy",
        breed="Husky",
        age=2,
        distanceMiles=2.7,
        available=True,
        energyLevel="high",
        bio="Dramatic howler. Looking for a co-star in the next zoomie sequel.",
        imageUrl="/api/static/dogs/ziggy.jpg",
    ),
    Profile(
        id="13",
        name="Cooper",
        breed="Standard Poodle",
        age=4,
        distanceMiles=1.1,
        available=True,
        energyLevel="high",
        bio="Fancy haircut, feral heart. Will absolutely steal your sock.",
        imageUrl="/api/static/dogs/cooper.jpg",
    ),
    Profile(
        id="14",
        name="Hazel",
        breed="Rottweiler",
        age=3,
        distanceMiles=2.2,
        available=False,
        energyLevel="medium",
        bio="Total softie with a tough-guy résumé. Leans on everyone she loves.",
        imageUrl="/api/static/dogs/hazel.jpg",
    ),
    Profile(
        id="15",
        name="Rocky",
        breed="Boxer",
        age=2,
        distanceMiles=0.7,
        available=True,
        energyLevel="high",
        bio="Bounces first, asks questions never. Great at greeting mailmen.",
        imageUrl="/api/static/dogs/rocky.jpg",
    ),
    Profile(
        id="16",
        name="Daisy",
        breed="Doberman",
        age=5,
        distanceMiles=3.4,
        available=True,
        energyLevel="medium",
        bio="Elegant on the outside, goofball on the inside.",
        imageUrl="/api/static/dogs/daisy.jpg",
    ),
    Profile(
        id="17",
        name="Finn",
        breed="Samoyed",
        age=1,
        distanceMiles=1.6,
        available=True,
        energyLevel="high",
        bio="Walking cloud. Smiles at strangers and sheds on them too.",
        imageUrl="/api/static/dogs/finn.jpg",
    ),
    Profile(
        id="18",
        name="Penny",
        breed="Cocker Spaniel",
        age=8,
        distanceMiles=0.5,
        available=False,
        energyLevel="low",
        bio="Senior sweetheart. Enjoys slow sniffy strolls and ear scratches.",
        imageUrl="/api/static/dogs/penny.jpg",
    ),
    Profile(
        id="19",
        name="Gizmo",
        breed="Pomeranian",
        age=3,
        distanceMiles=1.9,
        available=True,
        energyLevel="high",
        bio="Tiny but fearless. Barks at things ten times his size.",
        imageUrl="/api/static/dogs/gizmo.jpg",
    ),
    Profile(
        id="20",
        name="Stella",
        breed="Miniature Schnauzer",
        age=6,
        distanceMiles=2.8,
        available=True,
        energyLevel="medium",
        bio="Distinguished beard, undistinguished manners at dinnertime.",
        imageUrl="/api/static/dogs/stella.jpg",
    ),
    Profile(
        id="21",
        name="Murphy",
        breed="Alaskan Malamute",
        age=4,
        distanceMiles=3.1,
        available=False,
        energyLevel="high",
        bio="Built for snow, living in the suburbs. Dramatic about summer.",
        imageUrl="/api/static/dogs/murphy.jpg",
    ),
    Profile(
        id="22",
        name="Rosie",
        breed="Whippet",
        age=2,
        distanceMiles=1.3,
        available=True,
        energyLevel="high",
        bio="Zero to sprint in two seconds, then a long nap on the couch.",
        imageUrl="/api/static/dogs/rosie.jpg",
    ),
    Profile(
        id="23",
        name="Oscar",
        breed="Yorkshire Terrier",
        age=9,
        distanceMiles=0.2,
        available=False,
        energyLevel="low",
        bio="Grumpy old gentleman with a heart of gold. Hates the vacuum.",
        imageUrl="/api/static/dogs/oscar.jpg",
    ),
    Profile(
        id="24",
        name="Willow",
        breed="English Bulldog",
        age=5,
        distanceMiles=2.0,
        available=True,
        energyLevel="low",
        bio="Snorts when happy, which is always. Moves at her own pace.",
        imageUrl="/api/static/dogs/willow.jpg",
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

    try:
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

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An error occurred while compiling neighbor profiles."
        )

@app.get("/api/available-names", response_model=list[str])
def get_available_names():

    available_profiles = [p for p in profiles if p.available is True]

    return sorted([p.name for p in available_profiles])