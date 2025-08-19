from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# PostgreSQL database URL
# Example: "postgresql+psycopg2://user:password@host:port/db"
engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
