from dataclasses import dataclass, field
from uuid import UUID

from src.core.genre.domain.genre_repository import GenreRepository


@dataclass
class GenreOutput:
    id: UUID
    name: str
    categories: set[UUID]
    is_active: bool


class ListGenre:

    def __init__(self, genre_repository: GenreRepository):
        self.genre_repository = genre_repository

    @dataclass
    class Input:
        pass

    @dataclass
    class Output:
        data: list[GenreOutput] 

    def execute(self, request: Input) -> Output:
        genres = self.genre_repository.list()

        data = [
            GenreOutput(
                id=genre.id,
                name=genre.name,
                categories=genre.categories,
                is_active=genre.is_active,
            )
            for genre in genres
        ]

        return self.Output(data=data)
