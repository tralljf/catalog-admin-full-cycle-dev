import pytest
import uuid
from src.core.genre.domain.genre import Genre

class TestGenre():
    def test_name_is_required(self):
        with pytest.raises(TypeError):
            Genre()

    def test_name_must_have_256_characters_or_less(self):
        with pytest.raises(ValueError):
            Genre("a" * 257)

    def test_genre_id_is_a_uuid_invalid(self):
        genre = Genre(name="test")
        assert isinstance(genre.id, uuid.UUID)

    def test_genre_id_is_a_uuid(self):
        id = uuid.UUID('ac6cb88c-72e9-4301-b26f-c31bb9bdb7bd')
        genre = Genre(id=id, name="test")

        assert genre.id == id

    def teste_genre_id_is_valid(self):
        with pytest.raises(TypeError):
            Genre(name="test", id=1)
        with pytest.raises(TypeError):
            Genre(name="test", id="invalid")

    def test_genre_is_active(self):
        genre = Genre(name="test")
        assert genre.is_active is True

    def test_genre_is_not_active(self):
        genre = Genre(name="test", is_active=False)
        assert genre.is_active is False

    def test_genre_whith_default_values(self):
        genre = Genre(name="test")

        assert genre.name == "test"
        assert genre.is_active is True
        assert isinstance(genre.id, uuid.UUID)

class TesteUpdate():

    def test_change_name_with_name(self):
        genre = Genre(name="filme")

        genre.change_name(name="filme 2")
        assert genre.name == "filme 2"

    def test_validate_change_name_with_invalid_name(self):
        genre = Genre(name="filme")

        with pytest.raises(ValueError, match="Name is can't be empty"):
            genre.change_name(name="")


class TestActivate():
    def test_activate_Genre(self):
        genre = Genre(name="filme", is_active=False)

        genre.activate()
        assert genre.is_active is True


class TestDeactivate():
    def test_deactivate_Genre(self):
        genre = Genre(name="filme")

        genre.deactivate()
        assert genre.is_active is False        

class TestEquality():
    def test_genre_equality(self):
        identificador = uuid.uuid4()
        genre1 = Genre(id=identificador, name="filme")
        genre2 = Genre(id=identificador, name="filme 2")
        genre3 = Genre(id=identificador, name="filme 3")

        assert genre1 == genre2
        assert genre1 == genre3
        assert genre2 == genre3

    def test_genre_equality_with_different_id(self):
        genre1 = Genre(id=uuid.uuid4(), name="filme")
        genre2 = Genre(id=uuid.uuid4(), name="filme 2")

        assert genre1 != genre2

    def test_genre_equality_with_different_class(self):
        class OtherClass():
            pass
        
        indentificador = uuid.uuid4()
        genre1 = Genre(id=indentificador, name="filme")
        other = OtherClass()
        other.id = indentificador

        assert genre1 != other


    class TestAddCategory():
        def test_add_category(self):
            genre = Genre(name="filme")
            category_id = uuid.uuid4()

            genre.add_category(category_id)
            assert category_id in genre.categories


    class TestRemoveCategory():
        def test_remove_category(self):
            genre = Genre(name="filme")
            category_id = uuid.uuid4()

            genre.add_category(category_id)
            genre.remove_category(category_id)
            assert category_id not in genre.categories