import uuid
from django.db import models
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from robotsociety.roles import Role


class UserManager(BaseUserManager):
    def create_user(self, username, name, surname, password=None):
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            username=username,
            name=name,
            surname=surname
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, surname, password):
        user = self.create_user(username, name, surname, password)
        user.role = Role.ADMIN
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["name", "surname"]

    def __str__(self):
        return self.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable = False)
    content = models.TextField()
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=False) # because I am not going to run the AI in real time a custom time has to be set manually to make it seem like legit hours have gone by
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "post"
