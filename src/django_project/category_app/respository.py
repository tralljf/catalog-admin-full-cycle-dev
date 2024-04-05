from uuid import UUID
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.django_project.category_app.models import Category as CategoryModel


class DjangoORMCategoryRepository(CategoryRepository):
    def __init__(self, category_model: CategoryModel = CategoryModel):
        self.category_model = category_model

    def create(self, category: Category):
        self.category_model.objects.create(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active
        )

    def get_by_id(self, id: UUID) -> Category | None:
        try:
            category = self.category_model.objects.get(id=id)
            return Category(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active
            )
        except self.category_model.DoesNotExist:
            return None
        
    def update(self, input: Category) -> Category:
        category = self.category_model.objects.get(id=input.id)
        category.name = input.name
        category.description = input.description
        category.is_active = input.is_active
        category.save()
        return Category(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active
        )
    
    def delete(self, id: UUID):
        self.category_model.objects.get(id=id).delete()

    def list(self) -> list[Category]:
        categories = self.category_model.objects.all()
        return [
            Category(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active
            ) for category in categories
        ]