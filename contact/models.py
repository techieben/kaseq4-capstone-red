from django.db import models


class Contact(models.Model):
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=450)
    sender = models.EmailField()
    cc_myself = models.BooleanField()
