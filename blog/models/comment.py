from django.conf import settings
from django.db import models

from blog.models import Post

# Create your models here.
AppUser = settings.AUTH_USER_MODEL


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
