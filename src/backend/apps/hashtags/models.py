from django.db import models

# Create your models here.

class Hashtag(models.Model):
    name = models.CharField(max_length=20)
    tag = models.CharField(max_length=15)