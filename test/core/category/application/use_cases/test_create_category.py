from unittest.mock import MagicMock
import uuid

import pytest
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import InvalidCategoryData
from src.core.category.application.use_cases.create_category import CreateCategory, CreateCategoryRequest


class TestCreateCategory:
    def test_should_create_category_with_validate(self):
        mock_repository = MagicMock(CategoryRepository)

        request = CreateCategoryRequest(
            name='Category 1', 
            description='Description 1'
        )
        response = CreateCategory(mock_repository).execute(request)

        assert response.id is not None
        assert isinstance(response.id, uuid.UUID)

    def test_should_create_category_with_invalidate_data(self):
        mock_repository = MagicMock(CategoryRepository)
        request = CreateCategoryRequest(
            name='', 
            description='Description 1',
            is_active=False
        )
        with pytest.raises(InvalidCategoryData, match='Name is can\'t be empty'):
            CreateCategory(mock_repository).execute(request)
        