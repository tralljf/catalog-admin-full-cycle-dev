from dataclasses import dataclass, field
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import InvalidGenre, ReleatedCategoryNotFound
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


@dataclass
class GenreOutput:
    id: UUID
    name: str
    category_ids: set[UUID]
    is_active: bool


class ListGenre:

    def __init__(self, genre_repository: GenreRepository):
        self.genre_repository = genre_repository

    @dataclass
    class Output:
        data: list[GenreOutput] = field(default_factory=list)

    def execute(self) -> Output:
        genres = self.genre_repository.list()

        mapped_genres = [
            GenreOutput(
                id=genre.id,
                name=genre.name,
                category_ids=genre.categories,
                is_active=genre.is_active
            ) for genre in genres
        ]


        return self.Output(data=mapped_genres)

        