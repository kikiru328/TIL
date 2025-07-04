from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:todos@127.0.0.1:3306/todos"

engine = create_engine(DATABASE_URL, echo=True) #echo=True: print sqlalchemy query
SessionFactory = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
