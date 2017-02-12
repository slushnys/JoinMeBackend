from backend.apps.crm.authentication import ExpiringTokenAuthenticationSystem
from backend.apps.ems.models import Event, Location, Participant
from backend.apps.ems.serializers import EventSerializer, LocationSerializer, ParticipantSerializer
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class EventViewSet(viewsets.ModelViewSet):
    # This viewset is responsible for:
    # Creating an event by a single user: TODO
    # Listing events with a certain custom filtering for certain people: TODO
    # Delete a certain event (only by an owner of event or administrator): TODO
    # BUG: When creating an event - owner is a nested field - have to create

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [ExpiringTokenAuthenticationSystem]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print serializer.get_initial
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        # Check if the person requesting to delete the instance is authenticated
        # Check if the requestor is the owner of instance or an admin, if neither - STOP ACTION
        # If owner or admin, delete the instance.
        instance = self.get_object()
        # print request.user
        # print instance.owner
        if request.user == instance.owner or request.user.is_staff:
            self.perform_destroy(instance)
            response = status.HTTP_204_NO_CONTENT
        else:
            response = status.HTTP_400_BAD_REQUEST
        # self.perform_destroy(instance)
        return Response(status=response)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    authentication_classes = [ExpiringTokenAuthenticationSystem]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data.update({'account': request.auth.user.id})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

