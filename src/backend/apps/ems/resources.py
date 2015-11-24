from backend.apps.ems.models import Event
from backend.apps.ems.serializers import EventSerializer
from rest_framework import viewsets


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
