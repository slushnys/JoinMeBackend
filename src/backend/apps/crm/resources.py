from collections import OrderedDict

import requests
from backend.apps.crm.models import Account, FacebookAuthentication, ExpiringAuthenticationToken
from backend.apps.crm.serializers import AccountSerializer, FacebookAuthenticationSerializer, \
    ExpiringAuthenticationTokenSerializer
from backend.apps.ems.serializers import FacebookEventSerializer
from django.contrib.auth.hashers import make_password
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope, OAuth2Authentication
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_social_oauth2.authentication import SocialAuthentication


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        response = super(AccountViewSet, self).list(request, *args, **kwargs)
        return response


class FacebookAuthViewSet(viewsets.ModelViewSet):
    queryset = FacebookAuthentication.objects.all()
    serializer_class = FacebookAuthenticationSerializer
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        # here a access token should be inside request.data['access_token']
        short_lived_access_token = request.data.get('access_token', None)

        # Serializers
        token_serializer = ExpiringAuthenticationTokenSerializer
        account_serializer = AccountSerializer
        fb_auth_serializer = FacebookAuthenticationSerializer

        if short_lived_access_token:
            # if user passed an access token - a long-life access token could be retrieved!
            long_live_token_call = requests.get(url='https://graph.facebook.com/oauth/access_token',
                                                params={
                                                    'grant_type': 'fb_exchange_token',
                                                    'client_id': self.serializer_class.Meta.model.FACEBOOK_APP_KEY,
                                                    'client_secret': self.serializer_class.Meta.model.FACEBOOK_APP_SECRET,
                                                    'fb_exchange_token': short_lived_access_token,
                                                    'format': 'json'
                                                },
                                                headers={'Content-Type': 'application/json',
                                                         'Accept': 'application/json'}
                                                )
            if long_live_token_call.ok:
                json_long_lived_token = long_live_token_call.text.replace('&', '=').split('=')
                prolonged_token = {json_long_lived_token[0]: json_long_lived_token[1],
                                   json_long_lived_token[2]: json_long_lived_token[3]}
                # IF a return for a long-live token has been successful a request data copy is made and updated with long-live token.
                _data = OrderedDict()
                _data.update({'access_token': prolonged_token['access_token'],
                              'expires': prolonged_token['expires']})

                # Reformat some of the retrieved data for validation purposes
                information_retrieved = self.serializer_class.Meta.model.get_required_information(
                    passed_access_token=_data.get('access_token')).json()

                # Check if Facebook Authenticated user with this id already exist in the database
                try:
                    facebook_auth_lookup = FacebookAuthentication.objects.get(userid=information_retrieved['id'])
                except FacebookAuthentication.DoesNotExist:
                    # Create Facebook authentication instance and create Account instance
                    split_birthday = information_retrieved['birthday'].split('/')
                    information_retrieved['birthday'] = split_birthday[2] + "-" + \
                                                        split_birthday[0] + "-" + \
                                                        split_birthday[1]
                    information_retrieved['password'] = make_password(None)
                    information_retrieved['username'] = information_retrieved['email']

                    # Creating Account instance
                    account_serializer = account_serializer(data=information_retrieved)
                    if account_serializer.is_valid():
                        account_instance = account_serializer.create(account_serializer.validated_data)
                    else:
                        raise Exception(account_serializer.errors)

                    # Creating Facebook authentication instance
                    if account_instance:

                        # Format FB AUTH data
                        facebook_auth_data = dict()
                        facebook_auth_data.update(
                            {
                                'access_token': short_lived_access_token,
                                'user': account_instance.id,
                                'userid': information_retrieved['id'],
                                'expires': prolonged_token['expires'],
                                'long_lived_access_token': prolonged_token['access_token']
                            }
                        )

                        fb_auth_serializer = fb_auth_serializer(data=facebook_auth_data)
                        if fb_auth_serializer.is_valid():
                            auth_instance = fb_auth_serializer.create(fb_auth_serializer.validated_data)

                            # If user has been created successfully - check all the user events and add them to the database
                            # TODO: Put all the events which are retrieve from Facebook on ems system
                            # FINISHED: BELOW THE CREATION OF ALL FB EVENTS ON PARTICULAR USER
                            # fb_event_serializer = FacebookEventSerializer(data=auth_instance.retrieve_all_events())
                            # if fb_event_serializer.is_valid():
                            #     fb_event_serializer.create(validated_data=fb_event_serializer.validated_data)

                            # TODO: Create a token for this newly registered (logged in user)
                            # token_serializer = token_serializer(data={
                            #     'key': token_serializer.Meta.model().generate_key(),
                            #     'user': account_instance
                            # })
                            # if token_serializer.is_valid():
                            #     token_serializer.create(validated_data=token_serializer.validated_data)
                            token = ExpiringAuthenticationToken.objects.create(user=account_instance)
                            token.save()
                            return Response(
                                data={
                                    'facebook_access_token': fb_auth_serializer.data['long_lived_access_token'],
                                    'facebook_token_expires': fb_auth_serializer.data['expires'],
                                    'server_access_token': token.key,
                                    'server_token_expires': token.expires
                                },
                                status=200
                            )
                        else:
                            return Response(data=fb_auth_serializer.errors, status=400)

                else:
                    # If user has Facebook Authentication instance, create a new expiring token and return it
                    pass

            else:
                # Return of a long live token error
                # TODO: Have to allow also a short lived token probably
                return Response(data=long_live_token_call.json(), status=long_live_token_call.status_code)
