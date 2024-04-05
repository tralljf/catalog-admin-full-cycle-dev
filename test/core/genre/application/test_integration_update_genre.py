from unittest.mock import MagicMock
import uuid

import pytest
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.application.use_cases.update_genre import UpdateGenre, UpdateGenreRequest
from src.core.genre.domain.genre import Genre


class TestUpdateGenre:

    def test_update_genre_name(self):
        genre = Genre(
            name='Filme',
            is_active=False,
            categories={}
        )

        mock_repository = MagicMock(GenreRepository)
        mock_repository.get_by_id.return_value = genre
        
        use_case = UpdateGenre(mock_repository)
        request = UpdateGenreRequest(
            id=genre.id,
            name='Filme 2',
            categories={}
        )

        use_case.execute(request)

        assert genre.name == 'Filme 2'

        mock_repository.update.assert_called_once_with(genre)
        
    def test_can_activated_genre(self):
        genre = Genre(
            name='Filme',
            is_active=False
        )

        mock_repository = MagicMock(GenreRepository)
        mock_repository.get_by_id.return_value = genre
        
        use_case = UpdateGenre(mock_repository)
        request = UpdateGenreRequest(
            id=genre.id,
            is_active=True
        )

        use_case.execute(request)

        assert genre.name == 'Filme'
        assert genre.is_active == True

        mock_repository.update.assert_called_once_with(genre)

    def test_can_deactivated_genre(self):
        genre = Genre(
            name='Filme',
        )

        mock_repository = MagicMock(GenreRepository)
        mock_repository.get_by_id.return_value = genre
        
        use_case = UpdateGenre(mock_repository)
        request = UpdateGenreRequest(
            id=genre.id,
            is_active=False
        )

        use_case.execute(request)

        assert genre.name == 'Filme'
        assert genre.is_active == False

        mock_repository.update.assert_called_once_with(genre)

    def test_can_update_category_to_genre(self):
        genre = Genre(
            name='Filme',
            categories={uuid.uuid4()}
        )

        mock_repository = MagicMock(GenreRepository)
        mock_repository.get_by_id.return_value = genre


        category_ids = {uuid.uuid4(), uuid.uuid4()}
        
        use_case = UpdateGenre(mock_repository)
        request = UpdateGenreRequest(
            id=genre.id,
            categories=category_ids
        )

        use_case.execute(request)

        assert genre.name == 'Filme'
        assert genre.categories == category_ids

        mock_repository.update.assert_called_once_with(genre)

    def test_when_genre_not_found(self):
        genre = Genre(
            name='Filme',
            categories={uuid.uuid4()}
        )

        mock_repository = MagicMock(GenreRepository)
        mock_repository.get_by_id.return_value = None

        
        use_case = UpdateGenre(mock_repository)
        request = UpdateGenreRequest(
            id=uuid.uuid4(),
            name='Filme 2',
        )

        with pytest.raises(Exception) as exec_info:
            use_case.execute(request)

        assert str(exec_info.value) == 'Genre not found'

        
