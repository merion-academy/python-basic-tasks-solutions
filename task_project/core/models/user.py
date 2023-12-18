from flask_login import UserMixin
from sqlalchemy import Column, String
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from .database import db


class User(db.Model, UserMixin):
    def __init__(self, username: str):
        self.username = username

    username = Column(
        String(32),
        unique=True,
        index=True,
        nullable=False,
    )
    password_hash = Column(
        String,
        nullable=False,
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)
