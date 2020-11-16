from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    # required=False because of either username or email
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField()

    class Meta:
        app_label = 'safm_api'

    def validate(self, data):
        '''
        Validate the login.
        '''
        username = ''

        # Login with username
        if 'username' in data:
            username = data['username']
        # Login with email address
        elif 'email' in data:
            try:
                username = User.objects.get(email=data['email']).username
            except User.DoesNotExist:
                username = ''

        # Login with the given credentials
        user = authenticate(username=username, password=data['password'])

        if user:
            return user

        raise serializers.ValidationError('Wrong credentials')
