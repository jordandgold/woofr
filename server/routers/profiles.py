import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from pydantic import ValidationError
from sqlalchemy import Integer, cast, func, or_
from sqlmodel import Session, col, select

from db import get_session
from models import Profile, ProfileCreate, utcnow

UPLOADS_DIR = Path(__file__).parent.parent / "static" / "dogs" / "uploads"
DEFAULT_IMAGE_URL = "/api/static/dogs/default.svg"
ALLOWED_PHOTO_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}
MAX_PHOTO_BYTES = 5 * 1024 * 1024

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

def save_photo(photo: UploadFile) -> Path:
    """Store an uploaded photo in static/dogs/uploads under a server-generated name."""
    extension = ALLOWED_PHOTO_TYPES.get(photo.content_type or "")
    if extension is None:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Photo must be a JPEG, PNG or WebP image.",
        )

    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    destination = UPLOADS_DIR / f"{uuid4().hex}{extension}"
    written = 0

    with open(destination, "wb") as out:
        while chunk := photo.file.read(1024 * 64):
            written += len(chunk)
            if written > MAX_PHOTO_BYTES:
                out.close()
                destination.unlink(missing_ok=True)
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="Photo must be 5 MB or smaller.",
                )
            out.write(chunk)

    return destination


@router.post("/profiles", response_model=Profile, status_code=status.HTTP_201_CREATED)
def create_profile(
        name: str = Form(...),
        breed: str = Form(...),
        age: int = Form(...),
        distanceMiles: float = Form(...),
        available: bool = Form(...),
        energyLevel: str = Form(...),
        bio: str = Form(...),
        photo: UploadFile | None = File(None),
        session: Session = Depends(get_session),
    ):

    try:
        data = ProfileCreate(
            name=name.strip(),
            breed=breed.strip(),
            age=age,
            distanceMiles=distanceMiles,
            available=available,
            energyLevel=energyLevel,
            bio=bio.strip(),
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=[
                {"loc": err["loc"], "msg": err["msg"]}
                for err in e.errors(include_url=False, include_context=False, include_input=False)
            ],
        )

    saved_photo = save_photo(photo) if photo and photo.filename else None
    image_url = f"/api/static/dogs/uploads/{saved_photo.name}" if saved_photo else DEFAULT_IMAGE_URL

    try:
        # Ids are numeric strings; take the next one so ordering by id stays valid.
        max_id = session.exec(select(func.max(cast(Profile.id, Integer)))).one() or 0

        profile = Profile.model_validate(
            data,
            update={
                "id": str(max_id + 1),
                "favorited": False,
                "imageUrl": image_url,
                "created_at": utcnow(),
            },
        )
        session.add(profile)
        session.commit()
        session.refresh(profile)
    except Exception:
        session.rollback()
        if saved_photo:
            saved_photo.unlink(missing_ok=True)
        raise

    return profile
