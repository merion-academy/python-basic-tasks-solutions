# Самостоятельная работа №6

from datetime import date as date_type

import uvicorn
from fastapi import FastAPI, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from crud import fetch_rates
from models.db_session_async import get_async_session
from schemas import CurrencyRateOut

app = FastAPI()


@app.get(
    "/rates",
    response_model=CurrencyRateOut,
)
async def get_rates(
    from_currency: str,
    to_currency: str,
    date: date_type = Query(default_factory=date_type.today),
    session: AsyncSession = Depends(get_async_session),
):
    return await fetch_rates(
        session=session,
        date=date,
        from_currency=from_currency,
        to_currency=to_currency,
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
