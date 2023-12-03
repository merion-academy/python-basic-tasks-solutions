from sqlalchemy import (
    Column,
    String,
    DECIMAL,
    Date,
    UniqueConstraint,
)

from .base import Base


class CurrencyRate(Base):
    __tablename__ = "currency_rates"

    from_currency = Column(String, nullable=False)
    to_currency = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    rate = Column(DECIMAL, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            from_currency,
            to_currency,
            date,
            name="unique_pair_from_to_for_date",
        ),
    )
