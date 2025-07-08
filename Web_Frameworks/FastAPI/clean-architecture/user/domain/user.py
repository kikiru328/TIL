from dataclasses import dataclass
from datetime import datetime


# @dataclass
# class Profile:  # 데이터만 가지고 있음. id 없음 ==> Value Object (VO)
#     name: str
#     email: str


@dataclass  # 도메인 객체를 다루기 쉽게 함
class User:
    id: str
    # profile: Profile  # VO와 연동
    name: str
    email: str
    password: str
    created_at: datetime
    updated_at: datetime
