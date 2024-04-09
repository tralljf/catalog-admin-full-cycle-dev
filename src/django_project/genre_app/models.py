import uuid
from django.db import models

# Create your models here.
class Genre(models.Model):

    app_label = 'genre_app'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    categories = models.ManyToManyField('category_app.Category', related_name='genres')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "genre" 

    def __str__(self):
        return self.name
