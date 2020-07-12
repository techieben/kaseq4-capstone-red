from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.utils import timezone


class Author(AbstractUser):
    display_name = models.CharField(max_length=50, unique=True)
    following = models.ManyToManyField(
        'self', symmetrical=False, blank=True, related_name="followed_by")

    def __str__(self):
        return self.username
