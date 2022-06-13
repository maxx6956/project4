from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Posts")
    text = models.CharField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User, related_name="Likes")
    def __str__(self):
        return str(f"{self.poster} made a post @ {self.timestamp}")
    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "like": [poster.username for poster in self.like.all()]
        }

class Follow(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    follow = models.ManyToManyField(User, null=True, blank=True, related_name="Follows")
    def __str__(self):
        return str(self.account)