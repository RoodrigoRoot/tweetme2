from rest_framework import serializers
from .models import Tweet
from django.conf import settings

MAX_LENGTH = settings.MAX_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS

class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    action = serializers.CharField(required=True)
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in TWEET_ACTION_OPTIONS:
            raise  serializers.ValidationError("This is not a valid action for tweets")
        return value

class TweetCreateSerilizer(serializers.ModelSerializer):
    
    likes = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Tweet
        fields = ["id", "content", "likes"]
    
    def get_likes(self, obj):
        return obj.likes.count()

    def validate_content(self, value):
        if len(value) > settings.MAX_LENGTH:
            raise serializers.ValidationError("This tweet is too long")
        return value




class TweetSerilizer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    og_tweet = TweetCreateSerilizer(source="parent", read_only=True)

    class Meta:
        model = Tweet
        fields = ["id", "content", "likes", 'is_retweet', 'og_tweet']
    

    def get_likes(self, obj):
        return obj.likes.count()
