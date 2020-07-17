from django.db import models
from recipe.models import Recipe
from user.models import CustomUser
from review.models import Review


class Notification(models.Model):

    user_to = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='user_to'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    user_from = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='user_from',
        blank=True,
        null=True
    )
    text = models.CharField(max_length=150)

    REQUIRED_FIELDS = ['user_to', 'user_from', 'text']
