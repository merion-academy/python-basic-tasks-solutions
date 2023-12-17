from sqlalchemy import Column, String

from .database import db


class Quote(db.Model):
    text = Column(
        String,
        nullable=False,
        unique=True,
    )
