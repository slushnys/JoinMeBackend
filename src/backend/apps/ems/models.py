import uuid as uuid

from django.db import models

from backend.apps.crm.models import Account
from backend.apps.hashtags.models import Hashtag


class Event(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
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


class FacebookEvent(models.Model):
    description = models.TextField(blank=True)
    name = models.CharField(max_length=100)
    id = models.BigIntegerField(primary_key=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    place = models.ForeignKey('Place', null=True)
    attending_count = models.IntegerField(null=False, blank=True, default=0)
    timezone = models.CharField(max_length=50, null=True)
    updated_time = models.DateTimeField(null=True, blank=True)


class Participant(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
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


class Place(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey('Location')

# class Rule(models.Model):
#     name = models.CharField(max_length=20)
#

