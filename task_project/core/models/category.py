from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .database import db


class Category(db.Model):
    name = Column(
        String,
        nullable=False,
        unique=True,
    )
    description = Column(
        String,
        nullable=False,
        default="",
        server_default="",
    )

    movies = relationship(
        "Movie",
        back_populates="category",
        order_by="Movie.id",
    )
