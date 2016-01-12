import requests
from backend.apps.ems.models import Event, Location
from backend.apps.ems.serializers import EventSerializer, LocationSerializer
from oauth2_provider.ext.rest_framework import TokenHasScope, TokenHasReadWriteScope, OAuth2Authentication
from rest_framework import viewsets
from rest_framework_social_oauth2.authentication import SocialAuthentication


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [OAuth2Authentication, SocialAuthentication, ]
    # permission_classes = [TokenHasScope]
    # required_scopes = ['groups']

    def list(self, request, *args, **kwargs):
        user = request.user
        social = user.social_auth.get(provider='facebook')
        print social.extra_data['access_token']
        response = requests.get('https://graph.facebook.com/v2.5/me', data=
        {
            'access_token': social.extra_data['access_token'],
            'fields': 'email'
        }
                                )
        print response.content
        return super(EventViewSet, self).list(request, *args, **kwargs)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

