from dataclasses import dataclass, field
import uuid

@dataclass
class Category():

    name: str
    description: str = ""
    is_active: bool = True
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


    def update_category(self, name, description):
        self.name = name
        self.description = description
        self.validate()

    def activate(self):
        self.is_active = True
        self.validate()

    def deactivate(self):
        self.is_active = False
        self.validate()

    def __eq__(self, other):
        return self.id == other.id and self.__class__ == other.__class__