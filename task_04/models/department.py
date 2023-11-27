from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import Base


class Department(Base):
    name = Column(String)
    address = Column(String)

    employees = relationship(
        "Employee",
        back_populates="department",
        uselist=True,
    )
