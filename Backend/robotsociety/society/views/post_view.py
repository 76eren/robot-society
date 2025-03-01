import uuid
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response

from society.models import Post, User
from society.serializers.post_serializer import PostSerializer

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

@api_view(['POST'])
def create_post(request):
    serializer = PostSerializer(data=request.data)

    if serializer.is_valid():
        post = serializer.save()
        return Response({'message': 'Post created successfully', 'post_id': str(post.id)}, status=201)

    return Response(serializer.errors, status=400)



@api_view(['GET'])
def get_all_posts_by_user(request, username):
    if not User.objects.filter(username=username).exists():
        return Response({'error': 'User does not exist'}, status=404)

    user = User.objects.get(username=username)

    posts = Post.objects.filter(user=user)

    serializer = PostSerializer(posts, many=True)

    return Response(serializer.data, status=200)


@api_view(['GET'])
def get_post_by_id(request, user_id, post_id):
    pass

