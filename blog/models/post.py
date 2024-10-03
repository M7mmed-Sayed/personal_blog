from django.conf import settings
from django.db import models

from blog.models.category import Category
from blog.models.tag import Tag

# Create your models here.
AppUser = settings.AUTH_USER_MODEL


class Post(models.Model):
    """
       Represents a blog post to the author.
        The post can belong to at least one category
        The Post can have any numbers of tags may none
       """
    title = models.CharField(max_length=255)
    content = models.TextField()
    owner = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title


