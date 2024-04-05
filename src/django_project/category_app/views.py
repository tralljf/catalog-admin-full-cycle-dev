import uuid
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
)
from src.core.category.application.use_cases.create_category import CreateCategory, CreateCategoryRequest
from src.core.category.application.use_cases.delete_category import DeleteCategory, DeleteCategoryRequest
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest
    )

from src.core.category.application.use_cases.list_category import (
    ListCategory, 
    ListCategoryRquest, 
)
from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from src.django_project.category_app.respository import DjangoORMCategoryRepository
from src.django_project.category_app.serializer import CreateCategoryRequestSerializer, CreateCategoryResponseSerializer, DeleteCategoryRequestSerializer, ListCategoryResponseSerializer, RetrieveCategoryRequestSerializer, RetrieveCategoryResponseSerializer, UpdateCategoryRequestSerializer

class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        input = ListCategoryRquest()
        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        output = use_case.execute(input)

        response_serializer = ListCategoryResponseSerializer(output)

        return Response(
            status=HTTP_200_OK, 
            data=response_serializer.data
        )
    
    def retrieve(self, request: Request, pk=None) -> Response:
        serialzer = RetrieveCategoryRequestSerializer(data={'id': pk})
        serialzer.is_valid(raise_exception=True)
        
        use_case = GetCategory(repository=DjangoORMCategoryRepository())

        try:
            output = use_case.execute(request=GetCategoryRequest(id=serialzer.validated_data['id']))
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        serialzer = RetrieveCategoryResponseSerializer(instance=output)
    
        return Response(
            status=HTTP_200_OK,
            data=serialzer.data
        )
    
    def create(self, request: Request) -> Response:
        serializer = CreateCategoryRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(status=HTTP_400_BAD_REQUEST)
        
        use_case = CreateCategory(repository=DjangoORMCategoryRepository())

        input = CreateCategoryRequest(**serializer.validated_data)
        output = use_case.execute(request=input)

        serializer_output = CreateCategoryResponseSerializer(instance=output)

        return Response(
            status=HTTP_201_CREATED,
            data=serializer_output.data
        )
    
    def update(self, request: Request, pk=None) -> Response:
        serializer = UpdateCategoryRequestSerializer(data={**request.data, 'id': pk})
        serializer.is_valid(raise_exception=True)

        input = UpdateCategoryRequest(**serializer.validated_data)
        use_case = UpdateCategory(repository=DjangoORMCategoryRepository())
        try:
            use_case.execute(request=input)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_200_OK)


    def destroy(self, request: Request, pk=None) -> Response:
        serializer = DeleteCategoryRequestSerializer(data={'id': pk})
        serializer.is_valid(raise_exception=True)


        use_case = DeleteCategory(repository=DjangoORMCategoryRepository())
        input = DeleteCategoryRequest(**serializer.validated_data)
        try:
            use_case.execute(request=input)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        
        return Response(status=HTTP_204_NO_CONTENT)
