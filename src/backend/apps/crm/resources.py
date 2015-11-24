from backend.apps.crm.models import Account
from backend.apps.crm.serializers import AccountSerializer
from rest_framework import viewsets

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
