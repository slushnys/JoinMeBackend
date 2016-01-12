from rest_framework import serializers

from models import Event, Location


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location