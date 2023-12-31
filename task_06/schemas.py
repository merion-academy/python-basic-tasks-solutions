from datetime import date as date_type
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class CurrencyRateOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    from_currency: str
    to_currency: str
    rate: Decimal
    date: date_type
