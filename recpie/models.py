from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, null=True)
    bio = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Meal_Type(models.Model):
    HEARTHEALTHY = 'HH' 
    QUICKEASY = 'QE'
    lOWCALORIE = 'LC'
    GLUTENFREE = 'GF'
    DIABETIC= 'DA'
    VEGETARIAN = 'VG'

MEAL_CHOICES = [
    ('HH','Heart-Healthy'),
    ('QE','Quick&Easy'),
    ('LC','Low-Calorie'),
    ('GF','Gluten-Free'),
    ('DA','Diabetic'),
    ('VG','Vegetarian'),
]

def __str__(self):
    return self.meal_option


class RecpieItems(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    meal_option = models.CharField(max_length=2, choices=MEAL_CHOICES, default='Heart-Healthy')
    description = models.TextField()
    time_required = models.CharField(max_length=30)
    instructions = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    
    
    def __str__(self):
        return self.name
