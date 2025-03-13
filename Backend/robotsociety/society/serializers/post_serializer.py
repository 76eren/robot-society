from rest_framework import serializers

from society.models import Post, User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content', 'parent', 'created_at']
