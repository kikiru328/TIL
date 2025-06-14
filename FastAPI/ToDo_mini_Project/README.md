# FAST API : ToDo
Class: [실전! FastAPI 입문](https://www.inflearn.com/course/%EC%8B%A4%EC%A0%84-fastapi-%EC%9E%85%EB%AC%B8/dashboard)  
Contents: FastAPI를 활용하여 단순한 `CRUD`서비스가 아닌 실무 실습을 가정한 프로젝트 개발  

# 학습 내용 TIL

FastAPI 학습을 진행하면서 참고할 수 있는 내용들을 정리하고자 합니다.  

## Project Settings
### Setup
`poetry add fastapi, uvicorn`  
1. uvicorn은 fastapi를 실행시켜주는 도구
```bash
uvicorn main:app --reload #hot reloading
```
2. `localhost:port/docs`로 `swagger`문서 확인 가능  

## API
### GET
FastAPI의 API 중 조회는 `GET` Method를 사용한다.

1. 기본적인 `GET`의 형태는 다음과 같다.

```python
@app.get("~")
def get_handler_something():
    return things_we_need_to_get

@app.get("~/{id}")
def get_specific_something(id: int):
    return A_thing_we_need_to_get
```
2. sort나 query는 router에 입력이 아니라 함수 parameter로 입력된다

```python
@app.get("~")
def get_by_sort(order: str):
    data = list(data_from_db)
    if order == "DESC":
        return data[::-1]
    return data
```

### POST
생성하는 Method는 `POST`이다.  
생성하기 위해서는 `request body`가 필요한데,  
FastAPI는 `pydantic`을 이용해서 인자를 받아 생성한다.

```python
from pydantic import BaseModel

class what_we_need_to_create(BaseModel):
    id: int
    contents: str
    is_done: bool  

@app.post("~")
def create_handler(request: CreateToDoRequest):
    create_data[request.id] = request.dict()
    return create_data[request.id]
```

### PATCH
`PATCH`는 부분을 변경하는 method이다.  
일정 부분을 바꾸기 위해서 전체의 데이터를 불러오는 것이 아니라  
아래의 방법을 활용한다.

```python
from fastapi import Body

@app.patch("~/{id}")
def update_something(
    id: int,
    what: bool = Body(..., embed=True),
):
    something = data.get(id) # GET
    if something:
        something["what_value"] = what
        return something
    return {}
```

### DELETE
`DELETE`는 아예 삭제하는 method다.  
```python
@app.delete("~/{id}") 
def delete_this(id: int):
    data.pop(id, None)
    return data
```

## 상태코드

모든 web framework는 동일한 상태코드를 갖는다.  
- 200: OK, 요청 성공
- 201: Created, 요청 성공, POST
- 204: No Content: 요청 성공, 응답할 자원 없음
- 400: Bad Request: 요청 실패
- 401: Unauthorized: 인증실패
- 403: Forbidden: 권한 문제 및 잘못된 Method
- 404: Not Found: 자원이 없는 경우 & 잘못된 end point
- 500: Internal Server Error: 범용적 서버 에러
- 502: Bad Gateway: Reverse Proxy에서 서버의 응답을 처리할 수 없음
- 503: Service Unavailable: 서버가 요청을 처리할 수 없는 경우 (서버 다운)

### 상태 코드를 지정하는 법
```python
@app.get("~", status_code=200)
def ~

# FastAPI 활용할수도 있다
from fastapi import HTTPException

@ ~
def ~
    raise HTTPException(status_code=404, detail="not found")
```

## Database
모든 프로젝트의 database는 코드 내부에 저장하는게 아니라  
DB에 저장하게 될 것이다. 따라서 docker-mysql을 설정해 사용해보자.  

```bash
# docker mysql 설정
docker run -p 3306:3306 -e MYSQL_ROOT_PASSWORD=??? -e MYSQL_DATABASE=??? -d -v ???:/db --name ??? mysql:8.0

# MySQL 접속
docker exec -it ??? bash
mysql -u root -p 

# SQL
SHOW databases;
USE ~;
CREATE TABLE ~(
    ;
)
```

반면, 실제로 sqlalchemy를 사용할 경우 ORM에 의해서 테이블 생성, 데이터 조작이 가능하기에 이번 실습단위에서는 DB를 구축해두고 사용해보는 것으로 알아보자.  

기본적으로 sqlalchemy와 연동하기 위해서는 아래와 같은 connection이 필요하다

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:todos@127.0.0.1:3306/todos"

engine = create_engine(DATABASE_URL, echo=True) #echo=True: print sqlalchemy query
SessionFactory = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
```

## ORM
FastAPI와 MySql을 연동은 SQLAlchemy의 ORM으로 연동할 수 있다.  
ORM을 사용하는 이유는 직접 DB를 건드리지 않고 조회/생성/수정/삭제의 기능을  
FastAPI에서 사용할 수 있기 때문이다.  
(실제로 DB에 table이 구축되어 있지 않더라도 orm을 사용해서 table을 만들 수 있다.)

```python
from sqlalchemy import Column, Boolean, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Table(Base):
    __tablename__ = "Something"
    id = Column(Integer, ...)

    def __repr__(self):
        """조회시 출력되는 representive method"""
        return f"~~~"
```

