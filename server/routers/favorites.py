from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import Integer, cast
from sqlmodel import Session, col, select

from db import get_session
from models import Profile

router = APIRouter(prefix="/api/favorites", tags=["favorites"])

# Stored on the profile row itself, so favorites are shared by all visitors
# until there is a notion of a user.


def _get_profile(session: Session, profile_id: str) -> Profile:
    profile = session.get(Profile, profile_id)

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found.",
        )

    return profile


@router.get("", response_model=list[Profile])
def list_favorites(session: Session = Depends(get_session)):
    statement = (
        select(Profile)
        .where(col(Profile.favorited).is_(True))
        .order_by(cast(Profile.id, Integer))
    )

    return session.exec(statement).all()


@router.put("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def add_favorite(profile_id: str, session: Session = Depends(get_session)):
    profile = _get_profile(session, profile_id)
    profile.favorited = True
    session.add(profile)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(profile_id: str, session: Session = Depends(get_session)):
    profile = _get_profile(session, profile_id)
    profile.favorited = False
    session.add(profile)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
