from django.db import models

from backend.apps.crm.models import Account
from backend.apps.hashtags.models import Hashtag


class Event(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    description = models.TextField()
    status = models.IntegerField()
    location = models.ForeignKey('Location', null=True)
    owner = models.ForeignKey(Account, null=True)
    created = models.DateTimeField(auto_now=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    begin_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)


class Participants(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False)
    event = models.ForeignKey(Event)
    account = models.ForeignKey(Account)


class Hashtags(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False)
    event = models.ForeignKey(Event)
    hashtag = models.ForeignKey(Hashtag)


class Location(models.Model):
    name = models.CharField(max_length=30, null=True)
    street = models.CharField(max_length=100, null=True)
    postcode = models.CharField(max_length=6, null=True)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    longitude = models.FloatField(null=False)
    latitude = models.FloatField(null=False)
    state = models.CharField(max_length=50, null=True)

# class Rule(models.Model):
#     name = models.CharField(max_length=20)
#

