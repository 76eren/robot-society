from rest_framework import serializers

from society.models import Post, User


class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField()

    class Meta:
        model = Post
        fields = ['content', 'user', 'parent', 'created_at']

    def create(self, validated_data):
        user_username = validated_data.pop('user')

        try:
            user = User.objects.get(username=user_username)
        except User.DoesNotExist:
            raise serializers.ValidationError({"user": "User does not exist."})

        post = Post.objects.create(user=user, **validated_data)
        return post