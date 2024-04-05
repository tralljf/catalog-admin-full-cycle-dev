from dataclasses import dataclass, field
from uuid import UUID
import uuid

@dataclass
class Genre():

    name: str
    is_active: bool = True
    categories: set[UUID] = field(default_factory=set)
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        self.validate()

    def validate(self):
        if not self.name:
            raise ValueError("Name is can't be empty")

        if len(self.name) > 255:
            raise ValueError("Name must have 255 characters or less")
        
        if type(self.id) != uuid.UUID:
            raise TypeError("Category ID must be a UUID")


    def change_name(self, name):
        self.name = name
        self.validate()

    def activate(self):
        self.is_active = True
        self.validate()

    def deactivate(self):
        self.is_active = False
        self.validate()

    def add_category(self, category_id: UUID):
        self.categories.add(category_id)
        self.validate()

    def remove_category(self, category_id: UUID):
        self.categories.remove(category_id)
        self.validate()

    def __eq__(self, other):
        return self.id == other.id and self.__class__ == other.__class__