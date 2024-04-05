from unittest.mock import MagicMock
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.list_category import CategoryOutput, ListCategory, ListCategoryResponse
from src.core.category.domain.category import Category

class TestGetCategory:
    def test_should_get_category_with_validate(self):
        category1 = Category(
            name='Filme',
            description='Description 1',
            is_active=False
        )

        category2 = Category(
            name='Filme 2',
            description='Description 2',
            is_active=True
        )
        mock_repository = MagicMock(CategoryRepository)
        mock_repository.list.return_value = [category1, category2]
        

        response = ListCategory(mock_repository).execute()

        assert isinstance(response, ListCategoryResponse)
        assert response == ListCategoryResponse(
            data=[
                CategoryOutput(
                    id=category1.id,
                    name=category1.name,
                    description=category1.description,
                    is_active=category1.is_active
                ),
                CategoryOutput(
                    id=category2.id,
                    name=category2.name,
                    description=category2.description,
                    is_active=category2.is_active
                )
            ]
        )

        assert response.data[0].name == 'Filme'
        assert response.data[0].description == 'Description 1'
        assert response.data[0].is_active is False
        assert response.data[1].name == 'Filme 2'
        assert response.data[1].description == 'Description 2'
        assert response.data[1].is_active is True

        assert mock_repository.list.called

    def test_list_empity(self):
        mock_repository = MagicMock(CategoryRepository)
        mock_repository.list.return_value = []
        

        response = ListCategory(mock_repository).execute()


        assert response == ListCategoryResponse(data=[])