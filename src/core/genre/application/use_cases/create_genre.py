from dataclasses import dataclass, field
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.exceptions import InvalidGenre, ReleatedCategoryNotFound
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


class CreateGenre:

    def __init__(self, genre_repository: GenreRepository, 
                 category_repository: CategoryRepository):
        self.genre_repository = genre_repository
        self.category_repository = category_repository

    @dataclass
    class Input:
        name: str
        category_ids: set[UUID] = field(default_factory=set)
        is_active: bool = True

    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input) -> Output:
        category_ids = {category.id for category in self.category_repository.list()}
        if not input.category_ids.issubset(category_ids):
            raise ReleatedCategoryNotFound(f'Categories {input.category_ids - category_ids} not found')
        

        try:
            genre = Genre(
                name=input.name,
                categories=input.category_ids,
                is_active=input.is_active
            
            )
        except ValueError as e:
            raise InvalidGenre(e)
        
        self.genre_repository.create(genre)
        return self.Output(id=genre.id)