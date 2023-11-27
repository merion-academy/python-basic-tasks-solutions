from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    DateTime,
    func,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from .base import Base


class Employee(Base):
    full_name = Column(String, nullable=False)
    join_date = Column(
        DateTime,
        default=datetime.utcnow,
        server_default=func.now(),
    )
    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False,
        unique=False,
    )

    department = relationship(
        "Department",
        back_populates="employees",
        uselist=False,
    )
