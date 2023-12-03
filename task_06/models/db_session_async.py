from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

import config

async_engine: AsyncEngine = create_async_engine(
    config.DB_URL_ASYNC,
    echo=config.DB_ECHO,
)

async_session = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session
