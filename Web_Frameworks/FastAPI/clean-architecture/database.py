from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = (
    "mysql+mysqldb://root:test@127.0.0.1/fastapi-ca"  # connection schema
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,  # false auto save(commit)
    autoflush=False,
    bind=engine,
)

Base = declarative_base()
