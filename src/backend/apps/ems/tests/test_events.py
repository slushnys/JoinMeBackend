from collections import OrderedDict

from datetime import timedelta

from backend.apps.ems.models import Event, Location
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from backend.apps.crm.models import Account, FacebookAuthentication, ExpiringAuthenticationToken


class TestEMS(APITestCase):
    fixtures = ['fixture_events.json']

    def setUp(self):
        self.client = APIClient()

        self.facebook_key = getattr(settings, 'SOCIAL_AUTH_FACEBOOK_KEY', None)
        self.facebook_secret = getattr(settings, 'SOCIAL_AUTH_FACEBOOK_SECRET', None)
        self.user = Account.objects.create(name='Test User',
                                           first_name='Test',
                                           last_name='User',
                                           birthday='1991-05-02',
                                           email='test@socable.com',
                                           gender='male',
                                           username='test@socable.com',
                                           password=make_password(None),
                                           )

        self.auth = FacebookAuthentication()
        self.auth.userid = self.user.id
        self.auth.access_token = 'EAACvuLfpS4ABAE905TjEwZBfyWCO2EuZCLbWBXVRJCxqctDiyLXC9HjMtu6wCMp4s75KwkS9jDL59VvMYsFCYgYWWVpDEzZClSVhVwhSO84N4C8b54W3W64ucUcIGkSV3EetfILuIJpwpPtK2Qy1MlDG3k6aju25AJVZCUyiNwZDZD'
        self.auth.long_lived_access_token = 'EAACvuLfpS4ABAMLChO2w1BNYc4UsZBtOb82BP9YBLj3ncDJDjuh9uE5gtCid2mWkL1hxTRhTPDFjy04DFukltz2ASx4sSnEfCSOP8H5iU1BObwn27cBknNu1ZA48BQjAIC36HFs32ShMZAKNm9V3MgA3oL2iAIZD'

        self.server_auth_token = ExpiringAuthenticationToken.objects.create(user=self.user)

        # Create test events

    def test_already_existing_events(self):
        total_events = len(Event.objects.all())
        self.assertEquals(2, total_events)

    def test_get_all_events_w_o_authentication(self):
        # first need to create account - setup environment: DONE in setUp
        response = self.client.get('/api/v1/events/')
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_all_events_authenticated(self):
        response = self.client.get('/api/v1/events/', HTTP_AUTHORIZATION='Token {}'.format(self.server_auth_token.key))
        self.assertTrue(len(response.json()) > 1)

    def test_create_a_new_event(self):
        location_data = OrderedDict()
        location_data.update({
            'name': 'Covelakker Home House',
            'street': 'Covelakker',
            'postcode': '5625WG',
            'country': 'Netherlands',
            'city': 'Eindhoven',
            'longitude': '51.4689237',
            'latitude': '5.4817852',
        })
        event_data = OrderedDict()
        event_data.update({
            'name': 'BBQ Party',
            'capacity': 30,
            'description': 'Great garden BBQ Party with a DJ and a bartender!',
            'status': 1,
            'location': location_data,
            'owner': self.user.id,
            'begin_time': timezone.now() + timedelta(days=2),
            'end_time': timezone.now() + timedelta(days=3),
        })

        response = self.client.post('/api/v1/events/', data=event_data, format='json',
                                    HTTP_AUTHORIZATION='Token {}'.format(self.server_auth_token.key))

        self.assertEquals(status.HTTP_201_CREATED, response.status_code)

    def test_edit_an_event_when_owner(self):
        self.test_create_a_new_event()

        event_instance = Event.objects.first()

        new_event_data = {
            'name': 'Summer BBQ Party'
        }

        # PATCH equals UPDATE
        response = self.client.patch('/api/v1/events/{}/'.format(event_instance.uuid), data=new_event_data,
                                     format='json',
                                     HTTP_AUTHORIZATION='Token {}'.format(self.server_auth_token.key))

        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_delete_event_by_owner(self):
        self.test_create_a_new_event()
        event_instance = Event.objects.filter(name='BBQ Party').first()


        response = self.client.delete('/api/v1/events/{}/'.format(event_instance.uuid), format='json',
                                      HTTP_AUTHORIZATION='Token {}'.format(self.server_auth_token.key))
        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_join_event(self):
        self.test_create_a_new_event()

        event_instance = Event.objects.first()

        new_user = Account.objects.create(name='Test User #2',
                                          first_name='Test 2',
                                          last_name='User 2',
                                          birthday='1989-09-04',
                                          email='test2@socable.com',
                                          gender='female',
                                          username='test2@socable.com',
                                          password=make_password(None),
                                          )

        new_user_token = ExpiringAuthenticationToken.objects.create(user=new_user)

        request_data = {
            'event': event_instance.uuid,
            # 'account': new_user.id
        }

        response = self.client.post('/api/v1/participant/', data=request_data, format='json',
                                    HTTP_AUTHORIZATION='Token {}'.format(new_user_token.key))
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
