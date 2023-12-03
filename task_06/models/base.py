from sqlalchemy import (
    Column,
    Integer,
)
from sqlalchemy.orm import (
    DeclarativeBase,
)

# from sqlalchemy.ext.declarative import declarative_base
#
# Base = declarative_base()


class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True)
