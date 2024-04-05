from src.core.category.application.use_cases.create_category import CreateCategory, CreateCategoryRequest
from src.core.category.domain.category import Category
from src.core.category.infra.memory_category_repository import MemoryCategoryRepository


class TestListCategory:
    def test_should_list_category(self):
        repository = MemoryCategoryRepository()

        repository.create(Category(
            name='Filme',
            description='Description 1',
            is_active=False
        ))

        repository.create(Category(
            name='Filme 2',
            description='Description 2',
            is_active=True
        ))

        list = repository.list()

        assert len(list) == 2

    def test_list_empity(self):
        repository = MemoryCategoryRepository()

        list = repository.list()

        assert list == []