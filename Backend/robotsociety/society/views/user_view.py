from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from robotsociety.permissions import IsAdmin
from ..models import User
from ..serializers import UserSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def get_all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def get_user_by_id(request, user_id):
    user = get_object_or_404(User, id=user_id)
    serializer = UserSerializer(user)
    return Response(serializer.data)


