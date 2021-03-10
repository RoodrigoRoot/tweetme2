from django.db import models
import random
from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL

class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

class Tweet(models.Model):
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    likes = models.ManyToManyField(User, related_name="tweet_user", blank=True, through=TweetLike)
    image = models.FileField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.content

    @property
    def is_retweet(self):
        return self.parent != None
    
    class Meta:
        ordering = ["-id"]