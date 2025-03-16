import os
import uuid

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import datetime
from society.models import Post, User
from society.serializers.post_serializer import CreatePostSerializer, AllPostsSerializer
from dateutil.parser import parse
from dotenv import load_dotenv
import pytz


load_dotenv()
DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f%z"
timezone = pytz.utc

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    serializer = CreatePostSerializer(data=request.data)

    if serializer.is_valid():
        user = request.user

        content = serializer.validated_data.get('content')
        parent = serializer.validated_data.get('parent')

        created_at = ""

        # This way the AI can create posts at a custom time.
        # This is only meant for my AI to be able to call it, a regular user never has access to this
        if 'created_at' in serializer.validated_data and 'password_for_created_at' in serializer.validated_data:
            if serializer.validated_data.get('password_for_created_at') == os.getenv('CUSTOM_POST_TIME_PASSWORD'):
                created_at = serializer.validated_data.get('created_at')

        if created_at == "":
            created_at = datetime.datetime.now(tz=timezone).strftime(DATE_FORMAT)

        post = Post.objects.create(user=user, content=content, parent=parent, created_at=created_at)

        post.save()

        return Response({'message': 'Post created successfully'}, status=201)



@api_view(['GET'])
def get_all_posts_by_user(request, username):
    if not User.objects.filter(username=username).exists():
        return Response({'error': 'User does not exist'}, status=404)

    user = User.objects.get(username=username)

    posts = Post.objects.filter(user=user)

    serializer = AllPostsSerializer(posts, many=True)

    return Response(serializer.data, status=200)


# Creates the timetable for the front-end to view
@api_view(['GET'])
def get_all_posts_timetable(request):
    posts = Post.objects.all()

    serializer = AllPostsSerializer(posts, many=True)

    post_by_date = {}
    for post in serializer.data:
        date: str = post["created_at"]
        date_by_number: int = int(parse(date).timestamp())
        if date_by_number not in post_by_date:
            post_by_date[date_by_number] = []
        post_by_date[date_by_number].append(post)

    actual_posts = []
    for key in post_by_date:
        actual_posts.extend(post_by_date[key])

    return Response(actual_posts, status=200)


@api_view(['GET'])
def get_post_by_id(request, post_id):
    if not Post.objects.filter(id=uuid.UUID(post_id)).exists():
        return Response({'error': 'Post does not exist'}, status=404)

    post = Post.objects.get(id=uuid.UUID(post_id))
    serializer = AllPostsSerializer(post)

    return Response(serializer.data, status=200)


