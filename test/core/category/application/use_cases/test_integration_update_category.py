from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.domain.category import Category
from src.core.category.infra.memory_category_repository import MemoryCategoryRepository


class TestUpdateCategory:
    def test_should_update_category_with_validate(self):
        category = Category(
            name='Category 1', 
            description='Description 1',
            is_active=False
        )
        repository = MemoryCategoryRepository()
        repository.create(category)

        UpdateCategory(repository).execute(UpdateCategoryRequest(
            id=category.id,
            name='Category 2',
            description='Description 2',
            is_active=True
        ))

        category = repository.get_by_id(category.id)
        assert category.name == 'Category 2'
        assert category.description == 'Description 2'
        assert category.is_active is True
        