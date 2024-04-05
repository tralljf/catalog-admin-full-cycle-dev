
from src.core.category.infra.memory_category_repository import MemoryCategoryRepository
from src.core.category.domain.category import Category


class TestSave():
    def test_can_save_entity(self):
        category = Category(
            name='Category 1', 
            description='Description 1'
        )
        repository = MemoryCategoryRepository()
        repository.create(category)
        assert repository.categories[0] == category

class TestGetById():
    def test_can_get_entity_by_id(self):
        category = Category(
            name='Category 1', 
            description='Description 1'
        )
        repository = MemoryCategoryRepository()
        repository.create(category)
        assert repository.get_by_id(category.id) == category

    def test_can_not_get_entity_by_id(self):
        category = Category(
            name='Category 1', 
            description='Description 1'
        )
        repository = MemoryCategoryRepository()
        repository.create(category)
        assert repository.get_by_id('123') == None


class TestDelete():
    def test_can_delete_entity(self):
        category = Category(
            name='Category 1', 
            description='Description 1'
        )
        repository = MemoryCategoryRepository()
        repository.create(category)
        repository.delete(category.id)
        assert len(repository.categories) == 0
