import json
from decimal import Decimal
from datetime import date as date_type
from functools import partial

import aiohttp
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.currency_rates import CurrencyRate

API_URL = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/{date}/currencies/{from_currency}/{to_currency}.json"


loads_decimal = partial(json.loads, parse_float=Decimal)


async def fetch_currency_rate(
    date: date_type,
    from_currency: str,
    to_currency: str,
) -> dict[str, Decimal]:
    url = API_URL.format(
        date=date.isoformat(),
        from_currency=from_currency,
        to_currency=to_currency,
    )

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json(loads=loads_decimal)
            return data
            # data = await response.text()
            # json_data = json.loads(data, parse_float=Decimal)


async def get_currency_rate_from_db(
    session: AsyncSession,
    date: date_type,
    from_currency: str,
    to_currency: str,
):
    stmt = select(CurrencyRate).where(
        CurrencyRate.date == date,
        CurrencyRate.from_currency == from_currency,
        CurrencyRate.to_currency == to_currency,
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def save_rate_to_db(
    session: AsyncSession,
    date: date_type,
    from_currency: str,
    to_currency: str,
    rate: Decimal,
):
    rate = CurrencyRate(
        date=date,
        from_currency=from_currency,
        to_currency=to_currency,
        rate=rate,
    )
    session.add(rate)
    await session.commit()
    return rate


async def fetch_rates(
    session: AsyncSession,
    date: date_type,
    from_currency: str,
    to_currency: str,
) -> CurrencyRate:
    from_currency = from_currency.lower()
    to_currency = to_currency.lower()
    currency_rate: CurrencyRate | None = await get_currency_rate_from_db(
        session=session,
        date=date,
        from_currency=from_currency,
        to_currency=to_currency,
    )
    if currency_rate is not None:
        return currency_rate

    response_data = await fetch_currency_rate(
        date=date,
        from_currency=from_currency,
        to_currency=to_currency,
    )
    rate = response_data[to_currency]
    saved_rate: CurrencyRate = await save_rate_to_db(
        session=session,
        date=date,
        from_currency=from_currency,
        to_currency=to_currency,
        rate=rate,
    )

    return saved_rate
