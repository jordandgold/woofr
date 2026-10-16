from fastapi import APIRouter, HTTPException, status

from data import profiles
from models import Profile

router = APIRouter(prefix="/api", tags=["profiles"])

# Return all profiles when no filters are supplied.
# Match search against name or breed, ignoring case.
# Return only available profiles when availableOnly=true.
# Apply both conditions when both parameters are supplied.
# Return an empty array [] when no profiles match.

@router.get("/profiles", response_model=list[Profile])
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

@router.get("/available-names", response_model=list[str])
def get_available_names():

    available_profiles = [p for p in profiles if p.available is True]

    return sorted([p.name for p in available_profiles])
