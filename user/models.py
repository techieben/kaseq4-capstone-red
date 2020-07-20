from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    bio = models.CharField(max_length=450, blank=True)
    following = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='followed_by'
    )

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
