import uuid

import pytest
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.infra.memory_category_repository import MemoryCategoryRepository
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.memory_genre_repository import MemoryGenreRepository

@pytest.fixture
def movie_category() -> Category:
    return Category(name="movie")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="documentary")


@pytest.fixture
def genre_repository() -> MemoryGenreRepository:
    return MemoryGenreRepository()


@pytest.fixture
def category_repository(movie_category, documentary_category) -> CategoryRepository:
    return MemoryCategoryRepository(categories=[movie_category, documentary_category])

class TestUpdateGenre:

    def test_update_genre_name(self, genre_repository, category_repository):
        genre = Genre(
            name='Filme',
            is_active=False,
            categories={}
        )

        genre_repository.create(genre)
        
        use_case = UpdateGenre(
            genre_repository=genre_repository,
            category_repository=category_repository,
        )

        request = UpdateGenre.Input(
            id=genre.id,
            name='Filme 2',
            categories=set(),
            is_active=True
        )

        use_case.execute(request)

        genre_model = genre_repository.get_by_id(genre.id)

        assert genre_model.name == 'Filme 2'

    def test_can_update_category_to_genre(self, 
                                          genre_repository, category_repository):
        
        documentary_category = Category(name="Documentary")
        movie_category = Category(name="Movie")

        category_repository.create(documentary_category)
        category_repository.create(movie_category)
        
        genre = Genre(
            name='Filme',
            categories={documentary_category.id}
        )

        genre_repository.create(genre)
        category_ids = {documentary_category.id, movie_category.id}

        
        use_case = UpdateGenre(genre_repository=genre_repository, 
                               category_repository=category_repository)
        
        request = UpdateGenre.Input(
            id=genre.id,
            categories=category_ids,
            is_active=True,
            name='Filme',
        )

        use_case.execute(request)

        genre_model = genre_repository.get_by_id(genre.id)

        assert genre_model.categories == category_ids


    def test_when_genre_not_found(self, genre_repository, category_repository):
        
        use_case = UpdateGenre(
            genre_repository=genre_repository,
            category_repository=category_repository
        )
        
        request = UpdateGenre.Input(
            id=uuid.uuid4(),
            name='Filme',
            categories=set(),
            is_active=True 
        )

        with pytest.raises(Exception) as exec_info:
            use_case.execute(request)

        assert str(exec_info.value) == 'Genre not found'

        
