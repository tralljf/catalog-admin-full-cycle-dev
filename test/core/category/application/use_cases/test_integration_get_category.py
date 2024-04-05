import pytest
from src.core.category.application.use_cases.create_category import CreateCategory, CreateCategoryRequest
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest
from src.core.category.infra.memory_category_repository import MemoryCategoryRepository


class TestGetCategory:
    def test_should_get_category_with_validate(self):
        
        repository = MemoryCategoryRepository()

        request_new_category = CreateCategoryRequest(
            name='Category 1', 
            description='Description 1',
            is_active=False
        )
        response_new_category = CreateCategory(repository).execute(request_new_category)

        request = GetCategoryRequest(id=response_new_category.id)
        response = GetCategory(repository).execute(request)

        assert response.id is not None
        assert response.name == 'Category 1'
        assert response.description == 'Description 1'
        assert response.is_active is False

    def test_when_get_category_does_not_exist(self):
        repository = MemoryCategoryRepository()
        request = GetCategoryRequest(id='123e4567-e89b-12d3-a456-426614174000')

        with pytest.raises(CategoryNotFound, match='Category not found'):
            GetCategory(repository).execute(request)