from rest_framework import serializers
from .models import Tweet
from django.conf import settings

MAX_LENGTH = settings.MAX_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS

class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    action = serializers.CharField(required=True)

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in TWEET_ACTION_OPTIONS:
            raise  serializers.ValidationError("This is not a valid action for tweets")
        return value

class TweetSerilizer(serializers.ModelSerializer):
    
    class Meta:
        model = Tweet
        fields = ("content",) 
    
    def validate_content(self, value):
        if len(value) > settings.MAX_LENGTH:
            raise serializers.ValidationError("This tweet is too long")
        return value