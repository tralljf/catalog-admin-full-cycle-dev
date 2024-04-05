from unittest.mock import MagicMock
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.domain.category import Category


class TestUpdateCategory:

    def test_update_category_name(self):
        category = Category(
            name='Filme',
            description='Description 1',
            is_active=False
        )

        mock_repository = MagicMock(CategoryRepository)
        mock_repository.get_by_id.return_value = category
        
        use_case = UpdateCategory(mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name='Filme 2',
        )

        use_case.execute(request)

        assert category.name == 'Filme 2'
        assert category.description == 'Description 1'

        mock_repository.update.assert_called_once_with(category)

    def test_update_category_description(self):
        category = Category(
            name='Filme',
            description='Description 1',
        )

        mock_repository = MagicMock(CategoryRepository)
        mock_repository.get_by_id.return_value = category
        
        use_case = UpdateCategory(mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            description='Description 2',
        )

        use_case.execute(request)

        assert category.name == 'Filme'
        assert category.description == 'Description 2'

        mock_repository.update.assert_called_once_with(category)
        
    def test_can_activated_category(self):
        category = Category(
            name='Filme',
            description='Description 1',
            is_active=False
        )

        mock_repository = MagicMock(CategoryRepository)
        mock_repository.get_by_id.return_value = category
        
        use_case = UpdateCategory(mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            description='Description 1',
            is_active=True
        )

        use_case.execute(request)

        assert category.name == 'Filme'
        assert category.description == 'Description 1'
        assert category.is_active == True

        mock_repository.update.assert_called_once_with(category)

    def test_can_deactivated_category(self):
        category = Category(
            name='Filme',
            description='Description 1',
        )

        mock_repository = MagicMock(CategoryRepository)
        mock_repository.get_by_id.return_value = category
        
        use_case = UpdateCategory(mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            is_active=False
        )

        use_case.execute(request)

        assert category.name == 'Filme'
        assert category.description == 'Description 1'
        assert category.is_active == False

        mock_repository.update.assert_called_once_with(category)
