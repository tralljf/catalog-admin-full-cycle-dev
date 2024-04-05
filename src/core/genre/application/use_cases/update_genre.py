from dataclasses import dataclass, field
from uuid import UUID
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.application.exceptions import GenreNotFound


@dataclass
class UpdateGenreRequest:
    id: UUID
    name: str | None = None
    categories: set[UUID] = field(default_factory=set)
    is_active: bool | None = None
    

class UpdateGenre:

    def __init__(self, repository: GenreRepository):
        self.repository = repository
    
    def execute(self, request: UpdateGenreRequest) -> None:
        genre = self.repository.get_by_id(request.id)

        if genre is None:
            raise GenreNotFound('Genre not found')

        current_name = genre.name
        current_categories = genre.categories   
        
        if request.name is not None:
            current_name = request.name
        
        
        genre.change_name(
            name=request.name or current_name,
        )


        for category_id in current_categories.copy():
            genre.remove_category(category_id)

        for category_id in request.categories:
            genre.add_category(category_id)
        
        if request.is_active is not None:
            if request.is_active:
                genre.activate()
            else:
                genre.deactivate()

        if request.is_active is False:
            genre.deactivate()
        
        self.repository.update(genre)
        