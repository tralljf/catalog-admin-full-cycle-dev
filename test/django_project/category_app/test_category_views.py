import uuid
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from src.core.category.domain.category import Category
from src.django_project.category_app.respository import DjangoORMCategoryRepository


@pytest.fixture
def category_move():
    return Category(
        name='Filme',
        description='Filme description',
    
    )

@pytest.fixture
def category_serie():
    return Category(
        name='Serie',
        description='Serie description',
    
    )

@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()

@pytest.mark.django_db
class TestListApi():
    def test_list_categories(
        self,
        category_move: Category,
        category_serie: Category,
        category_repository: DjangoORMCategoryRepository
    ) -> None:

        category_repository.create(category_move)
        category_repository.create(category_serie)


        response = APIClient().get('/api/categories/')
        expected_data = { 
            'data': 
                [
                    {
                        'id': str(category_move.id),
                        'name': 'Filme',
                        'description': 'Filme description',
                        'is_active': True
                    },
                    {
                        'id': str(category_serie.id),
                        'name': 'Serie',
                        'description': 'Serie description',
                        'is_active': True
                    }
                ]
            }

        assert response.data == expected_data
        assert response.status_code == 200


@pytest.mark.django_db
class TestRetriveAPI:

    def test_retrieve_category_invalid_uuid(self):
        response = APIClient().get('/api/categories/1/')

        assert response.status_code == 400

    def test_retrieve_category(self):
        category = Category(
            name='Filme',
            description='Filme description',
        )

        repository = DjangoORMCategoryRepository()
        repository.create(category)

        response = APIClient().get(f'/api/categories/{category.id}/')
        expected_data = {'data': {
            'id': str(category.id),
            'name': 'Filme',
            'description': 'Filme description',
            'is_active': True
        }}

        assert response.data == expected_data
        assert response.status_code == 200



    def test_return_404_when_category_not_exists(self):
        url = f'/api/categories/64376e00-1fab-4242-a4d8-4d73123c20bf/'
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestCreateCategory:

    def test_when_payload_is_invalid_return_400(self) -> None:
        data = {
            'name': 'Filme',
        }

        response = APIClient().post('/api/categories/', data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


    def test_create_category(self, 
                             category_repository: DjangoORMCategoryRepository) -> None:
        data = {
            'name': 'Filme',
            'description': 'Filme description'
        }

        response = APIClient().post('/api/categories/', data=data)

        assert response.status_code == status.HTTP_201_CREATED

        created_category_id = uuid.UUID(response.data['id'])
        assert category_repository.get_by_id(created_category_id) == Category(
            id=created_category_id,
            name='Filme',
            description='Filme description'
        )
@pytest.mark.django_db
class TestUpdateCategory:

    def test_when_payload_is_invalid_return_400(self) -> None:
        data = {
            'name': 'Filme',
        }

        response = APIClient().put('/api/categories/1/', data=data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            'description': ['This field is required.'],
            'is_active': ['This field is required.'],
            'id': ['Must be a valid UUID.']
        }

    def test_update_category(self, 
                             category_repository: DjangoORMCategoryRepository) -> None:
        category = Category(
            name='Filme',
            description='Filme description'
        )
        
        category_repository.create(category)

        data = {
            'name': 'Filme 2',
            'description': 'Filme description 2',
            'is_active': True
        }

        response = APIClient().put(f'/api/categories/{category.id}/', data=data, format='json')

        assert response.status_code == status.HTTP_200_OK

        update_category = category_repository.get_by_id(category.id) 
        assert update_category.id == category.id
        assert update_category.name == 'Filme 2'
        assert update_category.description == 'Filme description 2'

    def test_when_category_does_not_exists(self):
        data = {
            'name': 'Filme',
            'description': 'Filme description',
            'is_active': True
        }

        response = APIClient().put('/api/categories/64376e00-1fab-4242-a4d8-4d73123c20bf/', data=data, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteCategory:

    def test_delete_when_category_does_not_exists(self):
        response = APIClient().delete('/api/categories/64376e00-1fab-4242-a4d8-4d73123c20bf/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_when_id_is_invalid(self):
        response = APIClient().delete('/api/categories/1/')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_category(self,
                            category_repository: DjangoORMCategoryRepository) -> None:
        category = Category(
            name='Filme',
            description='Filme description'
        )

        category_repository.create(category)

        response = APIClient().delete(f'/api/categories/{category.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert category_repository.get_by_id(category.id) is None