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