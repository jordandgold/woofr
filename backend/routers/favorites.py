from fastapi import APIRouter, HTTPException, Response, status

from data import profiles
from models import Profile

router = APIRouter(prefix="/api/favorites", tags=["favorites"])

# In-memory and shared by all visitors until there is a notion of a user.
favorite_ids: set[str] = set()


def _require_profile(profile_id: str) -> None:
    if not any(p.id == profile_id for p in profiles):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found.",
        )


@router.get("", response_model=list[Profile])
def list_favorites():
    return [p for p in profiles if p.id in favorite_ids]


@router.put("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def add_favorite(profile_id: str):
    _require_profile(profile_id)
    favorite_ids.add(profile_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(profile_id: str):
    _require_profile(profile_id)
    favorite_ids.discard(profile_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
