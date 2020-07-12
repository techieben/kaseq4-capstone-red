from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    display_name = models.CharField(max_length=50)
    bio = models.CharField(max_length=450)
    followers = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='following_user'
    )
    following = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='following_other'
    )
    
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email