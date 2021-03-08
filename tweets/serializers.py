from rest_framework import serializers
from .models import Tweet
from django.conf import settings

MAX_LENGTH = settings.MAX_LENGTH

class TweetSerilizer(serializers.ModelSerializer):
    
    class Meta:
        model = Tweet
        fields = ("content",) 
    
    def validate_content(self, value):
        if len(value) > settings.MAX_LENGTH:
            raise serializers.ValidationError("This tweet is too long")
        return value