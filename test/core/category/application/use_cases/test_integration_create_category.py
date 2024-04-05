import uuid
from src.core.category.application.use_cases.create_category import CreateCategory, CreateCategoryRequest
from src.core.category.infra.memory_category_repository import MemoryCategoryRepository


class TestCreateCategory:
    def test_should_create_category_with_validate(self):
        repository = MemoryCategoryRepository()

        request = CreateCategoryRequest(
            name='Category 1', 
            description='Description 1'
        )
        response = CreateCategory(repository=repository).execute(request)

        assert response.id is not None
        assert isinstance(response.id, uuid.UUID)
        assert len(repository.categories) == 1
        assert repository.categories[0].name == 'Category 1'

        persisted_category = repository.categories[0]
        assert persisted_category.id == response.id
        assert persisted_category.name == 'Category 1'
        assert persisted_category.description == 'Description 1'
        assert persisted_category.is_active is True


    def test_should_no_create_category_with_invalid_data(self):
        repository = MemoryCategoryRepository()

        request = CreateCategoryRequest(
            name='', 
            description='Description 1'
        )
        try:
            CreateCategory(repository=repository).execute(request)
            assert False
        except Exception as err:
            assert str(err) == 'Name is can\'t be empty'
            assert len(repository.categories) == 0

        assert len(repository.categories) == 0