import requests
from backend.apps.crm.models import Account, FacebookAuthentication
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from social.backends.facebook import FacebookOAuth2
from social.storage.django_orm import DjangoUserMixin
from social.strategies.django_strategy import DjangoStrategy


class AuthTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # self.test_user = User.objects.create_superuser(username='zslusnys', email='test@gmail.com', password='testpassword')
        # self.application = Application.objects.create(user=self.test_user,
        #                                               client_type='confidential',
        #                                               authorization_grant_type='password',
        #                                               )
        self.facebook_key = getattr(settings, 'SOCIAL_AUTH_FACEBOOK_KEY', None)
        self.facebook_secret = getattr(settings, 'SOCIAL_AUTH_FACEBOOK_SECRET', None)
        self.auth = FacebookAuthentication()
        self.auth.access_token = 'EAACvuLfpS4ABADyGd3zlZAe59Yt72AeXdZCrGep0efnEAGNH8z6remLwF7Alc7LtZCqAXZCArJZC2Ss8SGHqQvrql9eUJQCBer9E0xfUn0be1wNkqrlo6tXgl5OnZCMcyX9PGI02ry9Vl3VjbhNjjk6sCZAOr5ZAAhUZD'

    # def test_get_required_fields(self):
    #     backend = FacebookOAuth2()
    #
    #     strategy = DjangoStrategy(DjangoUserMixin)
    #
    #     backend.strategy = strategy
    #
    #     user_data = backend.user_data(self.issued_temp_token)
    #     # print user_data
    #
    #     # extra_data_request = requests.get(
    #     #     backend.USER_DATA_URL,
    #     #     params=dict(fields='events,birthday', access_token=self.issued_temp_token)
    #     # ).json()
    #     # print extra_data_request
    #
    #     response = self.client.get('/social/login/facebook/')
    #     print response.content
    #
    #     print Account.objects.all()

    def test_format_facebook_fields_for_request(self):
        self.assertEquals('id,name,email,first_name,last_name,birthday,picture,gender,events',
                          self.auth.format_requirements_for_request())

    def test_retrieve_facebook_requirements(self):
        self.auth.get_required_information(passed_access_token=self.auth.access_token)

    def test_create_user(self):
        response = self.client.post('/login/facebook/', data={'access_token': self.auth.access_token})
        print response

    def test_get_access_token(self):
        self.test_create_user()

        acc = Account.objects.first()
        # Account first has to be made and FacebookAuthentication created
        self.assertNotEqual(None, acc.get_access_token)

    def test_return_all_events(self):

        self.test_create_user()

        acc = Account.objects.first()

        auth_instance = acc.facebookauthentication_set.get(user_id=acc.id)
        self.assertEquals(status.HTTP_200_OK, auth_instance.retrieve_all_events().status)

    def test_create_a_token(self):
        self.test_create_user()

        acc = Account.objects.first()

        auth_instance = acc.facebookauthentication_set.get(user_id=acc.id)




