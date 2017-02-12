from datetime import datetime, timedelta

import requests
from django.contrib.auth.models import AbstractUser, UserManager
import binascii
import os

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

from rest_framework.authtoken.models import Token


class Account(AbstractUser):
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length=32, null=True)
    activation_token = models.CharField(max_length=50, null=True)
    account_token = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=100, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_access_token(self):
        auth_instance = self.facebookauthentication_set.get(user_id=self.id)
        if auth_instance:
            return auth_instance.return_access_token()
        else:
            print 'There\'s no authentication instance for this account'


class FacebookAuthentication(models.Model):
    access_token = models.CharField(null=False, blank=True, max_length=255)
    user = models.ForeignKey('Account')
    userid = models.CharField(max_length=32)
    expires = models.CharField(max_length=32, null=True, blank=True)
    long_lived_access_token = models.CharField(null=False, blank=True, max_length=255)

    objects = models.Manager()

    FACEBOOK_AUTH_VERSION = settings.FACEBOOK_API_VERSION
    FACEBOOK_AUTH_LINK = 'https://graph.facebook.com/v%s/me' % (FACEBOOK_AUTH_VERSION)
    FACEBOOK_APP_KEY = '193207894363008'
    FACEBOOK_APP_SECRET = '660848dc9ca623c9b80e356bd2081d1f'

    facebook_requirements = ['id', 'name', 'email', 'first_name', 'last_name', 'birthday', 'picture', 'gender',
                             'events', ]

    def return_access_token(self):
        # The logic behind this is that if the FacebookAuthentication instance exists, it means that one of the tokens must be present
        if self.long_lived_access_token:
            return self.long_lived_access_token
        else:
            return self.access_token

    def retrieve_all_events(self):
        event_requirements = ['id', 'attending_count', 'category,name', 'place', 'timezone', 'type', 'updated_time',
                              'start_time', 'end_time']
        # ATTENTION: Add since parameter with a unix-datetime stamp for retrieving events not older than now
        response = requests.get(self.FACEBOOK_AUTH_LINK + '/events/',
                                params={
                                    'fields': self.format_requirements_for_request(event_requirements),
                                    'access_token': self.return_access_token(),
                                    'since': datetime.now().strftime('%s'),
                                    'limit': 500
                                })
        if response.ok:
            return response
        else:
            raise Exception('Server was unable to retrieve events.')

    @classmethod
    def get_required_information(cls, passed_access_token=None):
        if passed_access_token:
            access_token = passed_access_token
        else:
            access_token = cls.access_token
        response = requests.get(cls.FACEBOOK_AUTH_LINK,
                                params={
                                    'fields': cls.format_requirements_for_request(cls.facebook_requirements),
                                    'access_token': access_token
                                }
                                )
        return response

    @classmethod
    def format_requirements_for_request(cls, requirement_list):
        field_string = ''
        for field in requirement_list:
            if requirement_list[len(requirement_list) - 1] == field:
                field_string += field
            else:
                field_string += field + ','

        return field_string


class ExpiringAuthenticationToken(models.Model):
    """
        The default authorization token model.
        """
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.OneToOneField(AUTH_USER_MODEL, related_name='auth_token',
                                on_delete=models.CASCADE, verbose_name=_("User"))
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    expires = models.DateTimeField(_("Expires"), default=datetime.now() + timedelta(days=180), null=False,
                                   blank=False)

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/tomchristie/django-rest-framework/issues/705
        verbose_name = _("Server Token")
        verbose_name_plural = _("Server Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(ExpiringAuthenticationToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
