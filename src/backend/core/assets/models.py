from backend.apps.ems.models import Event
from django.db import models


class Image(models.Model):
    name = models.CharField(max_length=50)
    event = models.ForeignKey(Event)
