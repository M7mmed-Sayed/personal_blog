from django.conf import settings
from django.db import models

from blog.models.post import Post

# Create your models here.
AppUser = settings.AUTH_USER_MODEL
class Like(models.Model):
    """
        Represents a like at the post from  the user.
           """
    owner = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner.first_name} {self.owner.last_name} likes on {self.post.title}"