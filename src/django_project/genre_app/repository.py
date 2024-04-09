from uuid import UUID
from django.db import transaction
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository
from src.django_project.genre_app.models import Genre as GenreModel


class DjangoORMGenreRepository(GenreRepository):
    def __init__(self, genre_model: GenreModel = GenreModel):
        self.genre_model = genre_model

    def create(self, input: Genre) -> None:
        with transaction.atomic():
            genre_model = self.genre_model.objects.create(
                id=input.id,
                name=input.name,
                is_active=input.is_active
            )
            genre_model.categories.set(input.categories)
        
    def get_by_id(self, id: UUID) -> Genre | None:
        try:
            genre_model = self.genre_model.objects.get(id=id) 
        except GenreModel.DoesNotExist:
            return None
        
        return Genre(
            id=genre_model.id,
            name=genre_model.name,
            is_active=genre_model.is_active,
            categories={category.id for category in genre_model.categories.all()}
        )
    
    def delete(self, id: UUID) -> None:
        self.genre_model.objects.filter(id=id).delete()
    
    def update(self, input: Genre) -> Genre:
        try:
            genre_model = self.genre_model.objects.get(id=input.id)
        except GenreModel.DoesNotExist:
            return None

        with transaction.atomic(): 
            self.genre_model.objects.filter(id=input.id).update(
                name=input.name,
                is_active=input.is_active
            )
            genre_model.categories.set(input.categories)            
    
    def list(self) -> list[Genre]:
        return [
            Genre(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
                categories=set(genre.categories.values_list("id", flat=True)),
            )
            for genre in self.genre_model.objects.all()
        ]