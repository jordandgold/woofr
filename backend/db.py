from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine, select

from data import seed_profiles
from models import Profile

DATABASE_URL = f"sqlite:///{Path(__file__).parent / 'woofr.db'}"

# check_same_thread=False lets FastAPI's threadpool share the SQLite connection.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def get_session():
    with Session(engine) as session:
        yield session


def seed_db(target_engine) -> None:
    """Insert the starter profiles if the table is empty."""
    with Session(target_engine) as session:
        if session.exec(select(Profile)).first() is None:
            session.add_all(Profile(**p.model_dump()) for p in seed_profiles)
            session.commit()


def init_db() -> None:
    SQLModel.metadata.create_all(engine)
    seed_db(engine)
