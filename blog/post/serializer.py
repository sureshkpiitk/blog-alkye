from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from post.models import Post, Comment


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "text", "post", 'auther', 'created']


class PostSerializer(ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'auther', 'created', 'comments']
