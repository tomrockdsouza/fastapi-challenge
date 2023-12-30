from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
import os

SEC_APP_DATABASE_CREDS = \
    f'{quote_plus(os.environ["POSTGRES_USER"])}:{quote_plus(os.environ["POSTGRES_PASSWORD"])}@' \
    f'{os.environ["POSTGRES_HOST"]}:{os.environ["POSTGRES_PORT"]}/{os.environ["POSTGRES_DB"]}'

DATABASE_URL = f"postgresql+asyncpg://{SEC_APP_DATABASE_CREDS}"
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, class_=AsyncSession, autoflush=False, bind=engine)

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

