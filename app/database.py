from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

_DB_CONNECTION_STRING = f"mysql+pymysql://{settings.database_user}:{settings.database_password}" \
                        f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(_DB_CONNECTION_STRING)  # creates DB connection
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # DB session for transactions
BaseEntity = declarative_base()
