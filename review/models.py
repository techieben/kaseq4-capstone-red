from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from user.models import CustomUser
from recipe.models import Recipe


class Voters(models.Model):
    model_choices = [
        ('Upvote', 'Upvote'),
        ('Downvote', 'Downvote'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    review = models.ForeignKey('Review', on_delete=models.CASCADE, related_name='review')
    vote = models.CharField(choices=model_choices, max_length=8)

    REQUIRED_FIELDS = ['user', 'vote']


class Review(models.Model):
    title = models.CharField(max_length=120)
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
        Voters,
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
