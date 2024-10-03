
from django.conf import settings
from django.db import models

# Create your models here.
AppUser = settings.AUTH_USER_MODEL

class Category(models.Model):
    """
          Represents a category for the posts.
          Each one has a unique name.
        """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

