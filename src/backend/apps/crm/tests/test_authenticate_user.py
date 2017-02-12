from datetime import datetime, timedelta

from backend.apps.crm.models import Account, ExpiringAuthenticationToken
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class TestEMS(APITestCase):
    fixtures = ['accounts_fixture.json', '../../ems/fixtures/fixture_events.json']

    def setUp(self):
        self.client = APIClient()

    def test_user_authorized(self):
        token = ExpiringAuthenticationToken.objects.create(user=Account.objects.first())
        response = self.client.get('/api/v1/events/', HTTP_AUTHORIZATION='Token {}'.format(token.key))
        self.assertEquals(status.HTTP_200_OK, response.status_code, response)

    def test_user_authorize_w_token_created_now(self):
        token = ExpiringAuthenticationToken.objects.create(user=Account.objects.first(),
                                                           created=datetime.utcnow(),
                                                           expires=timezone.now()+timedelta(hours=1))
        response = self.client.get('/api/v1/events/', HTTP_AUTHORIZATION='Token {}'.format(token.key))
        self.assertEquals(status.HTTP_200_OK, response.status_code, response)

    def test_user_authorize_w_token_expired(self):
        token = ExpiringAuthenticationToken.objects.create(user=Account.objects.first(),
                                                           created=datetime.utcnow(),
                                                           expires=timezone.now()-timedelta(hours=1))
        response = self.client.get('/api/v1/events/', HTTP_AUTHORIZATION='Token {}'.format(token.key))
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code, response)

    def test_user_unauthorized(self):
        token = '4a6s5df4d1fg3daf4g6a5fd4g6adf4g'
        response = self.client.get('/api/v1/events/', HTTP_AUTHORIZATION='Token {}'.format(token.key))
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_user_access_w_o_token(self):
        response = self.client.get('/api/v1/events/')
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, response.status_code)


