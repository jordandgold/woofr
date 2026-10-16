from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import Integer, cast, or_
from sqlmodel import Session, col, select

from db import get_session
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
        session: Session = Depends(get_session),
    ):

    try:
        statement = select(Profile).order_by(cast(Profile.id, Integer))

        if availableOnly:
            statement = statement.where(col(Profile.available).is_(True))

        if search:
            statement = statement.where(
                or_(
                    col(Profile.name).icontains(search, autoescape=True),
                    col(Profile.breed).icontains(search, autoescape=True),
                )
            )

        return session.exec(statement).all()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An error occurred while compiling neighbor profiles."
        )

@router.get("/available-names", response_model=list[str])
def get_available_names(session: Session = Depends(get_session)):

    statement = (
        select(Profile.name)
        .where(col(Profile.available).is_(True))
        .order_by(Profile.name)
    )

    return session.exec(statement).all()
