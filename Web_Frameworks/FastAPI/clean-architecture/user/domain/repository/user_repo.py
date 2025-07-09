# User 도메인을 영속화 하기 위한 모듈 -> IUserRepository --> Interface
# 이 인터페이스의 실제 구현체는 인프라 계층에 존재.

from abc import ABCMeta, abstractmethod

from user.domain.user import User


class IUserRepository(metaclass=ABCMeta):  # OOP Interface 선언
    @abstractmethod  # 추상 클래스 실제 구현은 infra에서
    def save(self, user: User) -> None:  # 구현체가 이 함수를 구현하지 않으면 에러
        raise NotImplementedError

    @abstractmethod
    def find_by_email(self, email: str) -> User:
        """
        이메일로 유저 검색
        검색한 유저가 없을 경우 422에러 발생
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User):
        raise NotImplementedError

    @abstractmethod
    def get_users(
        self, page: int, items_per_page: int
    ) -> tuple[int, list[User]]:  # pagination
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: str):
        raise NotImplementedError
