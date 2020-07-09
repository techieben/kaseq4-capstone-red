from django.db import models
from recpie.models import Author
from django.utils import timezone
# from django.contrib.postgres.fields import ArrayField
# from django.contrib.postgres.fields import JSONField


class Recipe(models.Model):
    MEAL_CHOICES = [
        ('HH','Heart-Healthy'),
        ('QE','Quick&Easy'),
        ('LC','Low-Calorie'),
        ('GF','Gluten-Free'),
        ('DA','Diabetic'),
        ('VG','Vegetarian'),
    ]
    
    title = models.CharField(max_length=120, unique=True)
    description = models.TextField(max_length=320)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author')
    favorites = models.ManyToManyField(
        Author,
        blank=True,
        symmetrical=False,
        related_name='user_favorite'
    )
    date_created = models.DateTimeField(default=timezone.now)
    # A list of CharField, or create a Tag class and make a many to many connection
    # tags = ArrayField(models.CharField(max_length=2, choices=MEAL_CHOICES), blank=True)
    # instructions = ArrayField(models.CharField(max_length=320))
    servings = models.IntegerField(default=1)
    # Save as a list [0,0,0]?, [days, hours, minuites]?
    time_prep_days = models.IntegerField(default=0)
    time_prep_hours = models.IntegerField(default=0)
    time_prep_mins = models.IntegerField(default=0)
    time_cook_days = models.IntegerField(default=0)
    time_cook_hours = models.IntegerField(default=0)
    time_cook_mins = models.IntegerField(default=0)
    time_additional_days = models.IntegerField(default=0)
    time_additional_hours = models.IntegerField(default=0)
    time_additional_mins = models.IntegerField(default=0)

    # reviews will point to a Recipe
    # stretch goals photos, public/private recipe, (property) avg ratings from reviews
    
    def __str__(self):
        return self.content

    @property
    def total_time(self):
        total_time_days = self.time_prep_days + self.time_hours_days + self.additional_prep_days
        total_time_hours = self.time_prep_hours + self.time_hours_hours + self.additional_prep_hours
        total_time_mins = self.time_prep_mins + self.time_hours_mins + self.additional_prep_mins
        running = True
        while running:
            running = False
            if total_time_mins >=60:
                total_time_hours += 1
                total_time_mins -= 60
                running = True
            if total_time_hours >=24:
                total_time_days += 1
                total_time_hours -= 24
                running = True
        output = ''
        if total_time_days > 0:
            output += total_time_days + ' Days '
        if total_time_hours > 0:
            output += total_time_hours + ' Hours '
        if total_time_mins > 0:
            output += total_time_mins + ' Mins'
        return (output)