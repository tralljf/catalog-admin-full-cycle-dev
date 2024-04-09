from dataclasses import dataclass, field
from uuid import UUID
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.application.exceptions import GenreNotFound, RelatedCategoriesNotFound



class UpdateGenre:

    def __init__(self, 
                 genre_repository: GenreRepository,
                 category_repository: CategoryRepository,
                 ):
        self.genre_repository = genre_repository
        self.category_repository = category_repository


    @dataclass
    class Input:
        id: UUID
        name: str
        is_active: bool
        categories: set[UUID]
    
    def execute(self, input: Input) -> None:
        genre = self.genre_repository.get_by_id(input.id)

        if genre is None:
            raise GenreNotFound('Genre not found')

        category_ids = {category.id for category in self.category_repository.list()}

        if not input.categories.issubset(category_ids):
            raise RelatedCategoriesNotFound(
                f"Categories with provided IDs not found: {input.categories - category_ids}")

        current_name = genre.name
        current_categories = genre.categories   
        
        if input.name is not None:
            current_name = input.name
        
        
        genre.change_name(
            name=input.name or current_name,
        )


        for category_id in current_categories.copy():
            genre.remove_category(category_id)

        for category_id in input.categories:
            genre.add_category(category_id)
        
        if input.is_active is not None:
            if input.is_active:
                genre.activate()
            else:
                genre.deactivate()

        if input.is_active is False:
            genre.deactivate()
        
        self.genre_repository.update(genre)
        