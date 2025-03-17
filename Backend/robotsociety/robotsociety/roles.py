from django.db import models

class Role(models.TextChoices):
    USER = 'User', 'user'
    ADMIN = 'Admin', 'admin'