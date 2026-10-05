import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("db_config")

# Load environment variables
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

DB_TYPE = os.getenv("DB_TYPE", "auto").lower()
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "VEDA@2007")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_DB = os.getenv("POSTGRES_DB", "vecicle_service")
SQLITE_DB = os.getenv("SQLITE_DB", "vehicle_service.db")

engine = None
ACTIVE_DB_TYPE = None

def get_engine():
    global engine, ACTIVE_DB_TYPE
    if engine is not None:
        return engine

    if DB_TYPE in ("postgres", "auto"):
        try:
            pg_url = URL.create(
                "postgresql+psycopg2",
                username=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                database=POSTGRES_DB,
            )
            test_engine = create_engine(pg_url, pool_pre_ping=True)
            # Test connectivity
            with test_engine.connect() as conn:
                pass
            engine = test_engine
            ACTIVE_DB_TYPE = "postgresql"
            logger.info(f"Connected to PostgreSQL database: '{POSTGRES_DB}' on {POSTGRES_HOST}:{POSTGRES_PORT}")
            return engine
        except Exception as e:
            if DB_TYPE == "postgres":
                logger.error(f"PostgreSQL connection failed: {e}")
                raise e
            logger.warning(
                f"PostgreSQL connection failed ({e}). Falling back to SQLite for seamless execution."
            )

    # SQLite fallback / standalone
    sqlite_path = BASE_DIR / SQLITE_DB
    sqlite_url = f"sqlite:///{sqlite_path}"
    engine = create_engine(
        sqlite_url,
        connect_args={"check_same_thread": False}
    )
    ACTIVE_DB_TYPE = "sqlite"
    logger.info(f"Connected to SQLite database: {sqlite_path}")
    return engine

engine = get_engine()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()