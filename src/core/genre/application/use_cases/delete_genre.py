from dataclasses import dataclass
from uuid import UUID

from src.core.genre.application.exceptions import GenreNotFound
from src.core.genre.domain.genre_repository import GenreRepository


class DeleteGenre:

    @dataclass
    class Input:
        id: UUID

    def __init__(self, repository: GenreRepository):
        self.repository = repository
    
    def execute(self, request: Input) -> None:
        genre = self.repository.get_by_id(request.id)

        if genre is None:
            raise GenreNotFound('Genre not found')
        
        self.repository.delete(genre.id)
