from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from user.models import CustomUser
from recipe.models import Recipe


class Review(models.Model):
    title = models.CharField(max_length=120)
    date = models.DateTimeField(default=timezone.now)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    content = models.TextField(max_length=320)
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    voters = models.ManyToManyField(
        CustomUser,
        blank=True,
        symmetrical=False,
        related_name='voters'
    )

    REQUIRED_FIELDS = [
        'title',
        'rating',
        'content',
        'author'
    ]

    class Meta:
        unique_together = ('author', 'recipe')

    def __str__(self):
        return self.title
