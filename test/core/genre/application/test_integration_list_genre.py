

from src.core.category.domain.category import Category
from src.core.category.infra.memory_category_repository import MemoryCategoryRepository
from src.core.genre.application.use_cases.list_genre import GenreOutput, ListGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.memory_genre_repository import MemoryGenreRepository


class TestListGenre:
    def test_list_genres_with_associated_category(self):
        category_repository = MemoryCategoryRepository()
        genre_repository = MemoryGenreRepository()

        movie_category = Category(
            name="Movie",
        )
        category_repository.create(movie_category)
        
        documentary_category = Category(
            name="Documentary",
        )
        category_repository.create(documentary_category)

        use_case = ListGenre(
            genre_repository=genre_repository,
        )

        genre = Genre(
            name="Action",
            categories={category.id for category in category_repository.list()},
            is_active=True
        )

        genre_repository.create(genre)

        output = use_case.execute(ListGenre.Input())

        assert len(output.data) == 1
        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=genre.id,
                    name="Action",
                    is_active=True,
                    categories={documentary_category.id, movie_category.id},
                )
            ]
        )

    def test_when_no_category_is_associated(self):
        genre_repository = MemoryGenreRepository()

        use_case = ListGenre(
            genre_repository=genre_repository,
        )

        genre = Genre(
            name="Action",
            categories=set(),
            is_active=True
        )

        genre_repository.create(genre)

        output = use_case.execute(ListGenre.Input())

        assert len(output.data) == 1
        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=genre.id,
                    name="Action",
                    is_active=True,
                    categories=set(),
                )
            ]
        )