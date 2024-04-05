import pytest
from src.core.category.application.use_cases.create_category import CreateCategory, CreateCategoryRequest
from src.core.category.application.use_cases.delete_category import DeleteCategory, DeleteCategoryRequest
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest
from src.core.category.infra.memory_category_repository import MemoryCategoryRepository


class TestDeleteCategory:
    def test_should_delete_category_with_validate(self):        
        repository = MemoryCategoryRepository()

        category_request = CreateCategoryRequest(
            name='Category 1', 
            description='Description 1',
            is_active=False
        )
        category_response = CreateCategory(repository).execute(category_request)


        assert repository.get_by_id(category_response.id) is not None

        request = DeleteCategoryRequest(id=category_response.id)
        response = DeleteCategory(repository).execute(request)

        assert response is None

        request_delete = GetCategoryRequest(id=category_response.id)
        with pytest.raises(CategoryNotFound, match='Category not found'):
            GetCategory(repository).execute(request_delete)

        assert repository.get_by_id(category_response.id) is None

    def test_when_delete_category_does_not_exist(self):
        repository = MemoryCategoryRepository()
        request = DeleteCategoryRequest(id='123e4567-e89b-12d3-a456-426614174000')

        with pytest.raises(CategoryNotFound, match='Category not found'):
            DeleteCategory(repository).execute(request)