from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .database import db


class Movie(db.Model):
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    category_id = Column(
        Integer,
        ForeignKey("category.id"),
        nullable=False,
    )

    category = relationship(
        "Category",
        back_populates="movies",
    )
