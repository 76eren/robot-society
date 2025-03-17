from rest_framework import serializers

from society.models import Post, User


class CreatePostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f%z", required=False)
    password_for_created_at = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Post
        fields = ['content', 'parent', 'created_at', 'password_for_created_at']


class AllPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'