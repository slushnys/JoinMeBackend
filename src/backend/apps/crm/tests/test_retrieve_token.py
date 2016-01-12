from django.contrib.auth.models import User
from oauth2_provider.models import Application, RefreshToken
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient


class AuthTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_user = User.objects.create_superuser(username='zslusnys', email='test@gmail.com', password='testpassword')
        self.application = Application.objects.create(user=self.test_user,
                                                      client_type='confidential',
                                                      authorization_grant_type='password',
                                                      )

    def test_get_token(self):
        data = {
            'client_id': self.application.client_id,
            'client_secret': self.application.client_secret,
            'username': 'zslusnys',
            'password': 'testpassword',
            'grant_type': 'password',
        }

        response = self.client.post('/auth/token', data=data)
        print response.content
        # request = requests.post('http://localhost:8008/auth/token', data=data)
        # print request.content

        # self.assertTrue(request.status_code == 200)

    def test_refresh_token(self):
        self.test_get_token()

        data={
            'client_id': self.application.client_id,
            'client_secret': self.application.client_secret,
            'refresh_token': RefreshToken.objects.get(user=self.test_user).token,
            'grant_type': 'refresh_token',
        }
        response = self.client.post('/auth/token', data=data)

        print(response.content)

    def test_convert_facebook_token(self):
        # self.test_get_token()
        #
        data={
            'client_id': self.application.client_id,
            'client_secret': self.application.client_secret,
            'grant_type': 'convert_token',
            'backend': 'facebook',
            'token': 'CAACTRvMEk3MBABkbRZBq9R6FZAO9TVZAtDs1sHHrjlWvHuIp3SrS6ATFZAQOGyjmeIFf6YzqChtdQMrei2s0IfLSxELRfTghPk0ft7AQXCuHEZCQF6q6DhxrD6ABhYLp5zmgRqlZBUCQuIOUMLZBh8N1jsbkbM32f2ZBIQY3K4Lwp3J6K3nfCbCptDytqm24eoS16i3AF75mte0xlZB10AAoB',
        }

        response = self.client.post('/auth/convert-token', data=data)

        print(response.content)

    def test_get_token_with_facebook_user(self):
        data={
            'grant_type': 'convert_token',
            'client_id': self.application.client_id,
            'client_secret': self.application.client_secret,
            'backend': 'facebook',
            'token': 'CAACvuLfpS4ABADbnweHvUgoEVzzrc7pG3bDwmPb7jkKrnXTXzHsHgQmHfrIVpZB6ehy0jq3nE5PYxoiPvV9ZBZAHNB8QW9KDbAxrZAF0RZAp7nL8eELC21YPx5SfwreTYTMARv97fqydl7WPXGyBo0EyQ5d3Wqno0T2Jq4qjDhJN9aYf4ipyatKGLtkZACjvchdzQJDfZA2q2znrYyPlM1O',

        }

        response = self.client.post('/auth/convert-token', data=data)
        print response.content

    def test_no_user_facebook_token(self):
        response = self.client.get('/api/v1/events/', follow=True,
                                   Authorization='Bearer facebook CAACEdEose0cBAPoA8WIfgZBrPFvwfXb1REUC7BoRfFlmW4ZCKiLmuOVujoYiY6GXmHVovfMR9P9UP5t5BdiGSmZBltB1ye7oCCmZBqd5jYuCYMyDm39oUmAYO5Hxqhwd9RvoyvZBb9NGicoZC4I6DaLIZBjjuRkrhczIfnmbox0geaVNlFoP93OBIWRZCP9TLfIVOjhuNRZBFabgbzM3dU00S',
                                   )
        print response.content