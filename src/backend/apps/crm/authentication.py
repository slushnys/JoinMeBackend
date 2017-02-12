from datetime import datetime

import pytz
from backend.apps.crm.models import ExpiringAuthenticationToken
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication


class ExpiringTokenAuthenticationSystem(TokenAuthentication):

    model = ExpiringAuthenticationToken

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        # This is required for the time comparison
        utc_now = datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        if token.expires < utc_now:
            raise exceptions.AuthenticationFailed(
                'Token was created at %s  but has expired at %s. Please authenticate again.' % (token.created, token.expires)
            )

        return token.user, token

