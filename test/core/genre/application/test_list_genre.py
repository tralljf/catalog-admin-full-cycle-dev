from unittest.mock import create_autospec
import uuid
import pytest

from src.core.category.domain.category import Category
from src.core.genre.application.use_cases.list_genre import GenreOutput, ListGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository

@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    return create_autospec(GenreRepository)

class TestListGenre:
    def test_list_genres_with_associated_category(self, mock_genre_repository):

        genre = Genre(
            name="Action",
            categories={},
            is_active=True
        )

        mock_genre_repository.list.return_value = [genre]

        use_case = ListGenre(
            genre_repository=mock_genre_repository,
        )

        output = use_case.execute()

        assert len(output.data) == 1
        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=genre.id,
                    name="Action",
                    is_active=True,
                    category_ids={},
                )
            ]
        )

    def test_list_genres_without_associated_category(self, mock_genre_repository): 

        category_id = uuid.uuid4()

        genre = Genre(
            name="Action",
            categories={category_id},
            is_active=True
        )

        mock_genre_repository.list.return_value = [genre]

        use_case = ListGenre(
            genre_repository=mock_genre_repository,
        )

        output = use_case.execute()

        assert len(output.data) == 1
        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=genre.id,
                    name="Action",
                    is_active=True,
                    category_ids={category_id},
                )
            ]
        )