from dependency_injector import containers, providers
from note.application.note_service import NoteService
from note.infra.repository.note_repo import NoteRepository
from user.application.user_service import UserService
from user.infra.repository.user_repo import UserRepository


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "user",  # package 전체. user.applications.user_service 처럼 단일 모듈 가능
            "note",
        ],
    )

    user_repo = providers.Factory(UserRepository)  # UseRepository Instance 생성 Factory
    user_service = providers.Factory(
        UserService, user_repo=user_repo
    )  # 생성하면서 user_repo 주입

    note_repo = providers.Factory(NoteRepository)
    note_service = providers.Factory(NoteService, note_repo=note_repo)
