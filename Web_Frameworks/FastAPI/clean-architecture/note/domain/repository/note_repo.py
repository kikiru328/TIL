from abc import ABCMeta, abstractmethod

from note.domain.note import Note


class INoteRepository(metaclass=ABCMeta):
    # user의 노트 전체 조회
    @abstractmethod
    def get_notes(
        self,
        user_id: str,
        page: int,
        items_per_page: int,
    ) -> tuple[int, list[Note]]:
        raise NotImplementedError

    # user의 노트 단일 조회
    @abstractmethod
    def find_by_id(self, user_id: str, id: str) -> Note:
        raise NotImplementedError

    # user의 노트 저장
    @abstractmethod
    def save(self, user_id: str, note: Note) -> Note:
        raise NotImplementedError

    # user의 단일 노트 수정
    @abstractmethod
    def update(self, user_id: str, note: Note) -> Note:
        raise NotImplementedError

    # user의 단일 노트 삭제
    @abstractmethod
    def delete(self, user_id: str, id: str):
        raise NotImplementedError

    # user 단일 노트의 tag 삭제
    @abstractmethod
    def delete_tags(self, user_id: str, note: Note):
        raise NotImplementedError

    # user tag_name으로 노트 전체 조회
    @abstractmethod
    def get_notes_by_tag_name(
        self,
        user_id: str,
        tag_name: str,
        page: int,
        items_per_page: int,
    ) -> tuple[int, list[Note]]:
        raise NotImplementedError
