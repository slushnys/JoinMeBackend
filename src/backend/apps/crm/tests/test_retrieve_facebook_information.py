from backend.apps.crm.models import Account, FacebookAuthentication
from backend.apps.ems.models import FacebookEvent
from backend.apps.ems.serializers import FacebookEventSerializer
from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

class FacebookInformationTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.facebook_key = getattr(settings, 'SOCIAL_AUTH_FACEBOOK_KEY', None)
        self.facebook_secret = getattr(settings, 'SOCIAL_AUTH_FACEBOOK_SECRET', None)
        self.user = Account(name='Test User',
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

    def test_return_all_events(self):
        acc = self.user
        auth_instance = self.auth
        self.assertEquals(status.HTTP_200_OK, auth_instance.retrieve_all_events().status_code)

    def test_save_all_events(self):
        acc = self.user
        auth_instance = self.auth

        retrieved_events = auth_instance.retrieve_all_events().json()

        fb_event_serializer = FacebookEventSerializer(data=retrieved_events['data'], many=True)

        if fb_event_serializer.is_valid():
            fb_event_serializer.create(fb_event_serializer.validated_data)
            self.assertTrue(FacebookEvent.objects.all() > 0)
        else:
            raise Exception(fb_event_serializer.errors)


