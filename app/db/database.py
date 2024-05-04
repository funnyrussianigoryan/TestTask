from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

async_engine = create_async_engine("sqlite+aiosqlite:///users_salary.db")

async_session = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


def get_session():
    return async_session()


async def get_db_session():
    session = get_session()
    try:
        yield session
    finally:
        await session.close()
