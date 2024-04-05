import pytest
import uuid
from src.core.category.domain.category import Category

class TestCategory():
    def test_name_is_required(self):
        with pytest.raises(TypeError):
            Category()

    def test_name_must_have_256_characters_or_less(self):
        with pytest.raises(ValueError):
            Category("a" * 257)

    def test_category_id_is_a_uuid_invalid(self):
        category = Category(name="test")
        assert isinstance(category.id, uuid.UUID)

    def test_category_id_is_a_uuid(self):
        id = uuid.UUID('ac6cb88c-72e9-4301-b26f-c31bb9bdb7bd')
        category = Category(id=id, name="test")

        assert category.id == id

    def teste_category_id_is_valid(self):
        with pytest.raises(TypeError):
            Category(name="test", id=1)
        with pytest.raises(TypeError):
            Category(name="test", id="invalid")

    def test_category_is_active(self):
        category = Category(name="test")
        assert category.is_active is True

    def test_category_is_not_active(self):
        category = Category(name="test", is_active=False)
        assert category.is_active is False

    def test_category_description(self):
        category = Category(name="test", description="test")
        assert category.description == "test"

    def test_category_description_is_empty(self):
        category = Category(name="test")
        assert category.description == ""


    def test_category_whith_default_values(self):
        category = Category(name="test")

        assert category.name == "test"
        assert category.description == ""
        assert category.is_active is True
        assert isinstance(category.id, uuid.UUID)

class TesteUpdate():

    def test_update_category_with_name_and_description(self):
        category = Category(name="filme", description="novo filme")

        category.update_category(name="filme 2", description="novo filme 2")
        assert category.name == "filme 2"
        assert category.description == "novo filme 2"

    def test_validate_update_category_with_invalid_name(self):
        category = Category(name="filme", description="novo filme")

        with pytest.raises(ValueError, match="Name is can't be empty"):
            category.update_category(name="", description="novo filme 2")


class TestActivate():
    def test_activate_category(self):
        category = Category(name="filme", description="novo filme", is_active=False)

        category.activate()
        assert category.is_active is True


class TestDeactivate():
    def test_deactivate_category(self):
        category = Category(name="filme", description="novo filme")

        category.deactivate()
        assert category.is_active is False        

class TestEquality():
    def test_category_equality(self):
        identificador = uuid.uuid4()
        category1 = Category(id=identificador, name="filme", description="novo filme")
        category2 = Category(id=identificador, name="filme 2", description="novo filme 2")
        category3 = Category(id=identificador, name="filme 3", description="novo filme 3")

        assert category1 == category2
        assert category1 == category3
        assert category2 == category3

    def test_category_equality_with_different_id(self):
        category1 = Category(id=uuid.uuid4(), name="filme", description="novo filme")
        category2 = Category(id=uuid.uuid4(), name="filme 2", description="novo filme 2")

        assert category1 != category2

    def test_category_equality_with_different_class(self):
        class OtherClass():
            pass
        
        indentificador = uuid.uuid4()
        category1 = Category(id=indentificador, name="filme", description="novo filme")
        other = OtherClass()
        other.id = indentificador

        assert category1 != other