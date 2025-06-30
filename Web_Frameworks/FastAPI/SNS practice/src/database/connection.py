from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL =  "mysql+pymysql://root:threads@127.0.0.1:3306/threads"

engine = create_engine(DATABASE_URL)

SessionFactory = sessionmaker(autocommit=False,
                              autoflush=False,
                              bind=engine)

# Generator (FastAPI의 Depends()에서 사용 가능)
def get_db():
    session = SessionFactory()
    try:
        yield session  # 요청 처리 중 DB 세션을 유지
    finally:
        session.close()  # 요청이 끝나면 DB 연결 종료