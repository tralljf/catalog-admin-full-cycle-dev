from unittest.mock import MagicMock
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest
from src.core.category.domain.category import Category



class TestGetCategory:
    def test_should_get_category_with_validate(self):
        category = Category(
            name='Filme',
            description='Description 1',
            is_active=False
        )
        mock_repository = MagicMock(CategoryRepository)
        mock_repository.get_by_id.return_value = category
        

        request = GetCategoryRequest(id=category.id)
        response = GetCategory(mock_repository).execute(request)

        assert response.id is not None
        assert response.name == 'Filme'
        assert response.description == 'Description 1'
        assert response.is_active is False
