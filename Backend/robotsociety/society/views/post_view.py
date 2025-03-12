import uuid

from rest_framework.decorators import api_view
from rest_framework.response import Response

from society.models import Post, User
from society.serializers.post_serializer import PostSerializer
from dateutil.parser import parse

DATE_FORMAT = "%d-%m-%y %H:%M:%S"

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


# Creates the timetable for the front-end to view
@api_view(['GET'])
def get_all_posts_timetable(request):
    posts = Post.objects.all()

    serializer = PostSerializer(posts, many=True)

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
    serializer = PostSerializer(post)

    return Response(serializer.data, status=200)


