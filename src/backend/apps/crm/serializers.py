from backend.apps.crm.models import Account, FacebookAuthentication, ExpiringAuthenticationToken
from rest_framework import serializers

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account


class FacebookAuthenticationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacebookAuthentication


class ExpiringAuthenticationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringAuthenticationToken
