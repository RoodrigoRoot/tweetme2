from django.db import models
import random
from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL

class Tweet(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.content

    def serialize(self):
        return {
            "id": self.id,
            "content":self.content,
            "likes":random.randint(0, 120)
        }
    
    class Meta:
        ordering = ["-id"]