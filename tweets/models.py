from django.db import models
import random
# Create your models here.

class Tweet(models.Model):
    content = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to='images/', null=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "content":self.content,
            "likes":random.randint(0, 120)
        }
    
    class Meta:
        ordering = ["-id"]