from backend.apps.crm.models import Account
from backend.apps.crm.serializers import AccountSerializer
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope, OAuth2Authentication
from rest_framework import viewsets
from rest_framework_social_oauth2.authentication import SocialAuthentication


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [TokenHasScope]
    authentication_classes = [OAuth2Authentication, SocialAuthentication]