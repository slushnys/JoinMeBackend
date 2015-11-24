from django.db import models

# Create your models here.

class Account(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    dob = models.DateField()
    activation_token = models.CharField(max_length=50)
    account_token = models.CharField(max_length=50)
    active = models.BooleanField()
