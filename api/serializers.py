from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Post,Like,Comment

class UserSerializer(serializers.ModelSerializer):
    
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    
    class Meta:
        model = User
        fields = [ 'username','following_count','followers_count']

    def get_following_count(self, obj):
        return obj.following.count()

    def get_followers_count(self, obj):
        return obj.followers.count()

class PostSerializer(serializers.ModelSerializer):

    class Meta:

        model = Post
        fields = ['id','creator','title','description','created_at']





class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('id','post','user')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['text']