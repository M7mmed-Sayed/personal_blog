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


class Tag(models.Model):
    """
          Represents a Tag for  posts.
          Each one has a unique name.
        """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


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


class Like(models.Model):
    """
        Represents a like at the post from  the user.
           """
    owner = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner.first_name} {self.owner.last_name} likes on {self.post.title}"


class Comment(models.Model):
    """
            Represents a comment at the post from  the user.
            """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner.first_name} {self.owner.last_name} commented on {self.post.title}"
