from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .util import get_env


class BaseModel(DeclarativeBase):
    pass

engine = create_engine(get_env("DATABASE_URL"))
Session = sessionmaker(engine)


def create_tables() -> None:
    BaseModel.metadata.create_all(engine)
