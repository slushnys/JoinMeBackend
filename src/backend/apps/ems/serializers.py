from apps.crm.serializers import AccountSerializer
from models import Event, Location, FacebookEvent, Participant
from rest_framework import serializers, exceptions
from django.utils.translation import ugettext_lazy as _


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        depth = 2


class EventSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=True)
    # owner = AccountSerializer(required=True)

    def create(self, validated_data):
        print validated_data
        location_data = validated_data.pop('location', None)
        if location_data:
            location_serializer = LocationSerializer(data=location_data)
            if location_serializer.is_valid():
                location_instance = location_serializer.create(validated_data=location_data)
                validated_data['location'] = location_instance
            else:
                raise exceptions.ValidationError(_(location_serializer.errors))
        return super(EventSerializer, self).create(validated_data)

    class Meta:
        model = Event
        depth = 2

class ParticipantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participant


class FacebookEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = FacebookEvent
        depth = 3

