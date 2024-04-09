import uuid
import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.infra.memory_category_repository import MemoryCategoryRepository
from src.core.genre.application.exceptions import InvalidGenre, ReleatedCategoryNotFound
from src.core.genre.application.use_cases.create_genre import CreateGenre
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


class TestCreateGenre:
    def test_create_genre_with_associate_categories(self, movie_category, documentary_category, category_repository):
        genre_repository = MemoryGenreRepository()

        use_case = CreateGenre(
            genre_repository=genre_repository,
            category_repository=category_repository,
        )

        input = CreateGenre.Input(name="Action", categories={movie_category.id, documentary_category.id})

        output = use_case.execute(input)

        assert output.id is not None
        saved_genre = genre_repository.get_by_id(output.id)

        assert saved_genre is not None
        assert saved_genre.name == "Action"
        assert saved_genre.categories == {movie_category.id, documentary_category.id}
        assert saved_genre.is_active is True

    def test_when_categories_do_not_exists_then_raise_relaited_category_not_found(self, movie_category, genre_repository):
        category_repository = MemoryCategoryRepository(categories=[movie_category])

        use_case = CreateGenre(genre_repository=genre_repository, category_repository=category_repository)

        category_id = uuid.uuid4()
        input = CreateGenre.Input(name="Action", categories={category_id})

        with pytest.raises(ReleatedCategoryNotFound):
            use_case.execute(input)

    def test_create_genre_without_categories(self, category_repository):
        genre_repository = MemoryGenreRepository()

        use_case = CreateGenre(
            genre_repository=genre_repository,
            category_repository=category_repository,
        )

        input = CreateGenre.Input(name="Action")

        output = use_case.execute(input)

        assert output.id is not None
        saved_genre = genre_repository.get_by_id(output.id)

        assert saved_genre is not None
        assert saved_genre.name == "Action"
        assert saved_genre.categories == set()
        assert saved_genre.is_active is True