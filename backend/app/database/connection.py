from sqlalchemy import create_engine

from app.config.settings import settings


DATABASE_URL = (
    f"mysql+pymysql://"
    f"{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:"
    f"{settings.DB_PORT}/"
    f"{settings.DB_NAME}"
)


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)