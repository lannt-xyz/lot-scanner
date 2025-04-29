from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from sqlmodel import create_engine, Session

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.entities.user import OAuthAccount, User
from config import settings

connect_args = {}
debug_mode = settings.sqlalchemy_echo == "True"
sync_db_url = settings.sqlalchemy_database_uri.replace("mysql+asyncmy://", "mysql+pymysql://")
engine = create_engine(sync_db_url,
                       pool_size=20,
                       max_overflow=10,
                       pool_timeout=30,
                       pool_recycle=1800,
                       echo=debug_mode,
                       connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

async_engine = create_async_engine(settings.sqlalchemy_database_uri)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)
