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

class RecpieItems(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.TextField()
    time_required = models.CharField(max_length=30)
    instructions = models.TextField()
    date = models.DateTimeField(default=timezone.now)
   
    
    def __str__(self):
        return self.name
