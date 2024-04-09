import pytest

from src.core.genre.domain.genre import Genre
from src.django_project.category_app.models import Category
from src.django_project.category_app.respository import DjangoORMCategoryRepository
from src.django_project.genre_app.models import Genre as GenreModel
from src.django_project.genre_app.repository import DjangoORMGenreRepository


@pytest.mark.django_db
class TestSave:
    def test_save_genre_in_database(self):
        genre = Genre(
            name='Genre 1',
        )

        repository = DjangoORMGenreRepository()

        assert GenreModel.objects.count() == 0
        repository.create(genre)
        assert GenreModel.objects.count() == 1

        genre_db = GenreModel.objects.get(id=genre.id)
        assert genre_db.id == genre.id
        assert genre_db.name == 'Genre 1'
        assert genre_db.is_active is True

    def test_save_genre_with_category_in_database(self):
        repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()

        category = Category(name="Action")
        category_repository.create(category)

        genre = Genre(name="Movie")
        genre.add_category(category.id)

        assert GenreModel.objects.count() == 0
        repository.create(genre)
        assert GenreModel.objects.count() == 1

        saved_genre = GenreModel.objects.get()
        assert saved_genre.categories.count() == 1

        related_category = saved_genre.categories.get()
        assert related_category.id == category.id


@pytest.mark.django_db
class TestUpdate:
    def test_update_genre_in_database(self):
        genre_repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()

        movie_category = Category(name="Movie")
        category_repository.create(movie_category)

        comedia = Genre(name="Movie")
        comedia.add_category(movie_category.id)
        genre_repository.create(comedia)


        serie_category = Category(name="Serie")
        category_repository.create(serie_category)

        comedia.add_category(serie_category.id)

        genre_repository.update(comedia)

        saved_genre = GenreModel.objects.get()
        assert saved_genre.categories.count() == 2

@pytest.mark.django_db
class TestDelete:
    def test_delete_genre_in_database(self):
        repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()

        category = Category(name="Action")
        category_repository.create(category)

        genre = Genre(name="Movie")
        genre.add_category(category.id)

        assert GenreModel.objects.count() == 0
        repository.create(genre)
        assert GenreModel.objects.count() == 1

        repository.delete(genre.id)

        assert GenreModel.objects.count() == 0


@pytest.mark.django_db
class TestList:
    def test_list_genre_in_database(self):
        repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()

        category = Category(name="Action")
        category_repository.create(category)

        genre = Genre(name="Movie")
        genre.add_category(category.id)

        repository.create(genre)

        assert len(repository.list()) == 1
        saved_genre = repository.list()[0]
        assert saved_genre.categories == {category.id}
        assert saved_genre.name == "Movie"
        assert saved_genre.is_active is True