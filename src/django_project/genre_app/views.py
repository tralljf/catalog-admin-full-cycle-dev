
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from src.core.genre.application.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.application.use_cases.list_genre import ListGenre
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.django_project.category_app.respository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.genre_app.serializer import CreateGenreInputSerializer, CreateGenreOutputSerializer, DeleteGenreInputSerializer, ListGenreOutputSerializer, UpdateGenreInputSerializer

class GenreViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        
        use_case = ListGenre(genre_repository=DjangoORMGenreRepository())
        output: ListGenre.Input = use_case.execute(ListGenre.Input())
        response_serializer = ListGenreOutputSerializer(output)

        return Response(
            status=status.HTTP_200_OK,
            data=response_serializer.data,
        )

    def create(self, request) -> Response:
        serializer = CreateGenreInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        use_case = CreateGenre(
            genre_repository=DjangoORMGenreRepository(), 
            category_repository=DjangoORMCategoryRepository()
        )
        try:
            output = use_case.execute(CreateGenre.Input(**serializer.validated_data))
        except (InvalidGenre) as error:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": str(error)},
            )

        return Response(
            status=status.HTTP_201_CREATED,
            data=CreateGenreOutputSerializer(output).data,
        )
        

    def update(self, request, pk=None):
        try:
            serializer = UpdateGenreInputSerializer(data={**request.data, 'id': pk})
            serializer.is_valid(raise_exception=True)

            
            input = UpdateGenre.Input(**serializer.validated_data)
            use_case = UpdateGenre(
                genre_repository=DjangoORMGenreRepository(),
                category_repository=DjangoORMCategoryRepository(),
            )
            use_case.execute(input)
        except GenreNotFound:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": f"Genre with id {pk} not found"},
            )
        except (InvalidGenre, RelatedCategoriesNotFound) as error:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": str(error)},
            )
        except ValueError as error:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": error},
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
        

    def destroy(self, request, pk=None) -> Response:
        serializer = DeleteGenreInputSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)
        
        use_case = DeleteGenre(repository=DjangoORMGenreRepository())
    
        try:
            use_case.execute(DeleteGenre.Input(id=pk))
        except Exception as error:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": str(error)},
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
        