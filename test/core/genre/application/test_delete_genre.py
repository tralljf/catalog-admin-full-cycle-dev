from unittest.mock import create_autospec

from src.core.genre.application.use_cases.delete_genre import DeleteGenre

from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


class TestDeleteGenre:
    def test_should_delete_genre_with_validate(self):
        genre = Genre(
            name='Filme',
            categories={},
            is_active=False
        )
        mock_repository = create_autospec(GenreRepository)
        mock_repository.get_by_id.return_value = genre

        use_case = DeleteGenre(mock_repository)
        use_case.execute(DeleteGenre.Input(id=genre.id))
        
        mock_repository.delete.assert_called_once_with(genre.id)

        