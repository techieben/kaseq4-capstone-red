from django.db import models
from django import forms
from user.models import CustomUser
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
# from django.contrib.postgres.fields import JSONField
from django import template

register = template.Library()


# source https://blogs.gnome.org/danni/2016/03/08/multiple-choice-using-djangos-postgres-arrayfield/
class ChoiceArrayField(ArrayField):
    """
    A field that allows us to store an array of choices.
    Uses Django's Postgres ArrayField
    and a MultipleChoiceField for its formfield.
    """

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.MultipleChoiceField,
            'choices': self.base_field.choices,
        }
        defaults.update(kwargs)
        # Skip our parent's formfield implementation completely as we don't
        # care for it.
        # pylint:disable=bad-super-call
        return super(ArrayField, self).formfield(**defaults)

class RecipeCard(models.Model):
    title = models.CharField(max_length=120, unique=True)
    recipe_picture = models.URLField(max_length=200)

class Recipe(models.Model):
    MEAL_CHOICES = [
        ('HH', 'Heart-Healthy'),
        ('QE', 'Quick&Easy'),
        ('LC', 'Low-Calorie'),
        ('GF', 'Gluten-Free'),
        ('DA', 'Diabetic'),
        ('VG', 'Vegetarian'),
    ]

    title = models.CharField(max_length=120, unique=True)
    description = models.TextField(max_length=320)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='custom_user')
    favorited_by = models.ManyToManyField(
        CustomUser,
        blank=True,
        related_name='favorites'
    )
    date_created = models.DateTimeField(default=timezone.now)
    # A list of CharField, or create a Tag class and make a many to many connection
    tags = ChoiceArrayField(models.CharField(
        max_length=2, choices=MEAL_CHOICES), blank=True)
    ingredients = ArrayField(models.CharField(max_length=450))
    instructions = ArrayField(models.CharField(max_length=320))
    servings = models.IntegerField(default=1)
    # Save as a list [0,0,0], [days, hours, minuites]
    time_prep = ArrayField(models.IntegerField(default=0), size=3)
    time_cook = ArrayField(models.IntegerField(default=0), size=3)
    time_additional = ArrayField(models.IntegerField(default=0), size=3)

    REQUIRED_FIELDS = [
        'title',
        'description',
        'author',
        'ingredients',
        'instructions',
        'servings',
        'time_prep',
        'time_cook',
        'time_additional'
    ]
    # reviews will point to a Recipe
    # stretch goals photos, public/private recipe, (property) avg ratings from reviews

    def __str__(self):
        return self.title

    @property
    def total_time(self):
        total_time_days = self.time_prep[0] + \
            self.time_cook[0] + self.time_additional[0]
        total_time_hours = self.time_prep[1] + \
            self.time_cook[1] + self.time_additional[1]
        total_time_mins = self.time_prep[2] + \
            self.time_cook[2] + self.time_additional[2]
        running = True
        while running:
            running = False
            if total_time_mins >= 60:
                total_time_hours += 1
                total_time_mins -= 60
                running = True
            if total_time_hours >= 24:
                total_time_days += 1
                total_time_hours -= 24
                running = True
        output = ''
        if total_time_days > 0:
            output += str(total_time_days) + ' Days '
        if total_time_hours > 0:
            output += str(total_time_hours) + ' Hours '
        if total_time_mins > 0:
            output += str(total_time_mins) + ' Mins'
        return (output)

    def plain_time(self, time_list):
        default_output = 'Not Specified'
        output = default_output
        if time_list[0] > 0:
            output = str(time_list[0]) + ' Days '
        if time_list[1] > 0:
            if output == default_output:
                output = str(time_list[1]) + ' Hours '
            else:
                output += str(time_list[1]) + ' Hours '
        if time_list[2] > 0:
            if output == default_output:
                output = str(time_list[2]) + ' Mins '
            else:
                output += str(time_list[2]) + ' Mins '
        return (output)

    @register.filter
    def related_plain_time(obj, time_list):
        return obj.get_related_plain_time(time_list)
