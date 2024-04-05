import pytest
from src.core.category.domain.category import Category
from src.core.category.infra.memory_category_repository import MemoryCategoryRepository
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.application.use_cases.delete_genre import DeleteGenre, DeleteGenreRequest
from src.core.genre.application.exceptions import GenreNotFound
from src.core.genre.infra.memory_genre_repository import MemoryGenreRepository

@pytest.fixture
def movie_category() -> Category:
    return Category(name="movie")

class TestDeleteGenre:
    def test_should_delete_genre_with_validate(self, movie_category):        
        repository = MemoryGenreRepository()
        category_repository = MemoryCategoryRepository()

        category_repository.create(movie_category)

        genre_request = CreateGenre.Input(
            name='Genre 1', 
            is_active=False,
            category_ids={movie_category.id}
        )

        genre_response = CreateGenre(
            genre_repository=repository,
            category_repository=category_repository
        ).execute(genre_request)


        assert repository.get_by_id(genre_response.id) is not None

        request = DeleteGenreRequest(id=genre_response.id)
        response = DeleteGenre(repository).execute(request)

        assert response is None
        assert repository.get_by_id(genre_response.id) is None

    def test_when_delete_genre_does_not_exist(self):
        repository = MemoryGenreRepository()
        request = DeleteGenreRequest(id='123e4567-e89b-12d3-a456-426614174000')

        with pytest.raises(GenreNotFound, match='Genre not found'):
            DeleteGenre(repository).execute(request)