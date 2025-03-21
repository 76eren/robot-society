import pytz
from datetime import datetime, tzinfo

from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from robotsociety.authentication import CookieJWTAuthentication
from ..models import User
from ..serializers import UserSerializer


@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        name = serializer.validated_data.get('name')
        surname = serializer.validated_data.get('surname')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({"error": "User already exists"}, status=status.HTTP_409_CONFLICT)

        user = User.objects.create_user(username=username, name=name, surname=surname, password=password)

        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    if request.user.is_authenticated:
        return Response({"error": "User is already logged in"}, status=status.HTTP_400_BAD_REQUEST)

    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    if user is None:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.check_password(password):
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    user.last_login = datetime.now(tz=pytz.UTC)
    user.save()

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    response = Response({"message": "Login successful"})

    combined_token = f"access={access_token}; refresh={refresh_token}"

    response.set_cookie(
        key=settings.SIMPLE_JWT["AUTH_COOKIE"],
        value=CookieJWTAuthentication.encrypt(combined_token),
        httponly=True,
        secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
        samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"]
    )

    return response


@api_view(['POST'])
def logout_user(request):
    response = Response({"message": "Logged out successfully"})
    response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])
    response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])
    return response
