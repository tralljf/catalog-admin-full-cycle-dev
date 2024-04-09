from unittest.mock import MagicMock
import uuid

import pytest
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.application.use_cases.update_genre import UpdateGenre
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

        mock_category_repository = MagicMock(CategoryRepository)
        
        use_case = UpdateGenre(
            genre_repository=mock_repository, 
            category_repository=mock_category_repository
        )

        request = UpdateGenre.Input(
            id=genre.id,
            name='Filme 2',
            categories=set(),
            is_active=True
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

        mock_category_repository = MagicMock(CategoryRepository)
        
        use_case = UpdateGenre(genre_repository=mock_repository, category_repository=mock_category_repository)
        request = UpdateGenre.Input(
            id=genre.id,
            is_active=True,
            categories=set(),
            name='Filme' 
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

        mock_category_repository = MagicMock(CategoryRepository)
        
        use_case = UpdateGenre(genre_repository=mock_repository, category_repository=mock_category_repository)
        request = UpdateGenre.Input(
            id=genre.id,
            is_active=False,
            categories=set(),
            name='Filme'
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

        mock_category_repository = MagicMock(CategoryRepository)

        movie_category = Category(
            name="Movie",
            id=uuid.uuid4()
        )

        documentary_category = Category(
            name="Documentary",
            id=uuid.uuid4()
        )

        category_ids = {documentary_category.id, movie_category.id}


        mock_category_repository.list.return_value = [movie_category, documentary_category]


        
        use_case = UpdateGenre(genre_repository=mock_repository, category_repository=mock_category_repository)
        request = UpdateGenre.Input(
            id=genre.id,
            categories=category_ids,
            is_active=True,
            name='Filme'
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

        mock_category_repository = MagicMock(CategoryRepository)
        
        use_case = UpdateGenre(genre_repository=mock_repository, category_repository=mock_category_repository)
        request = UpdateGenre.Input(
            id=uuid.uuid4(),
            name='Filme 2',
            categories=set(),
            is_active=True
        )

        with pytest.raises(Exception) as exec_info:
            use_case.execute(request)

        assert str(exec_info.value) == 'Genre not found'

        
