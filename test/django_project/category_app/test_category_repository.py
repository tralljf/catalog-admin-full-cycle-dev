import pytest

from src.core.category.domain.category import Category
from src.django_project.category_app.respository import DjangoORMCategoryRepository
from django_project.category_app.models import Category as CategoryModel


@pytest.mark.django_db
class TestSave:
    def test_save_category_in_database(self):
        category = Category(
            name='Category 1',
            description='Category 1 description',
        )

        repository = DjangoORMCategoryRepository()

        assert CategoryModel.objects.count() == 0
        repository.create(category)
        assert CategoryModel.objects.count() == 1

        category_db = CategoryModel.objects.get(id=category.id)
        assert category_db.id == category.id
        assert category_db.name == 'Category 1'
        assert category_db.description == 'Category 1 description'
        assert category_db.is_active is True


@pytest.mark.django_db
class TestUpdate:
    def test_update_category_in_database(self):
        category = Category(
            name='Category 1',
            description='Category 1 description',
        )

        repository = DjangoORMCategoryRepository()
        
        repository.create(category)
        
        category_db = CategoryModel.objects.get(id=category.id)
        category.name = 'Category 2'
        category.description = 'Category 2 description'
        category.is_active = False

        repository.update(category)

        category_db = CategoryModel.objects.get(id=category.id)
        assert category_db.id == category.id
        assert category_db.name == 'Category 2'
        assert category_db.description == 'Category 2 description'
        assert category_db.is_active is False

@pytest.mark.django_db
class TestDelete:
    def test_delete_category_in_database(self):
        category = Category(
            name='Category 1',
            description='Category 1 description',
        )

        repository = DjangoORMCategoryRepository()
        repository.create(category)

        assert CategoryModel.objects.count() == 1
        repository.delete(category.id)
        assert CategoryModel.objects.count() == 0

@pytest.mark.django_db
class TestList:
    def test_list_categories_in_database(self):
        category1 = Category(
            name='Category 1',
            description='Category 1 description',
        )
        category2 = Category(
            name='Category 2',
            description='Category 2 description',
        )

        repository = DjangoORMCategoryRepository()
        repository.create(category1)
        repository.create(category2)

        categories = repository.list()

        assert len(categories) == 2
        assert categories[0].id == category1.id
        assert categories[0].name == 'Category 1'
        assert categories[0].description == 'Category 1 description'
        assert categories[0].is_active is True
        assert categories[1].id == category2.id
        assert categories[1].name == 'Category 2'
        assert categories[1].description == 'Category 2 description'
        assert categories[1].is_active is True