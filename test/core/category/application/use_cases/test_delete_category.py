from unittest.mock import MagicMock, create_autospec
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.delete_category import DeleteCategory, DeleteCategoryRequest
from src.core.category.domain.category import Category



class TestDeleteCategory:
    def test_should_delete_category_with_validate(self):
        category = Category(
            name='Filme',
            description='Description 1',
            is_active=False
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = DeleteCategory(mock_repository)
        use_case.execute(DeleteCategoryRequest(id=category.id))
        
        mock_repository.delete.assert_called_once_with(category.id)

        