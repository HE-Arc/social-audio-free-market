from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from safm_api.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        write_only=True, # In case of user profile public email set to false
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    password_current = serializers.CharField(
        write_only=True,
        required=False
    )
    password_min_length = 8

    class Meta:
        app_label = 'safm_api'
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'password_confirm',
            'password_current',
            'date_joined'
        ]

    def validate(self, data):
        '''
        Validate the password fields for the creation of a
        new user or for a password patch.
        '''
        password = data.get('password')
        password_confirm = data.get('password_confirm')
        password_current = data.get('password_current')

        # User create or user password patch
        if not self.partial or (self.partial and password):
            # Password patch, but invalid current password
            if self.partial and not check_password(password_current, self.instance.password):
                raise serializers.ValidationError('Invalid current password.')

            # Password patch, but new password not different thant current one
            if self.partial and check_password(password, self.instance.password):
                raise serializers.ValidationError('The new password must be different than the current one.')

            # Password cannot be smaller thant 'password_min_length'
            if len(password) < self.password_min_length:
                raise serializers.ValidationError('Password length must be at least {0} characters.'.format(self.password_min_length))

            # Password (or new password) different than the confirm one
            if password != password_confirm:
                raise serializers.ValidationError('Password confirmation does not match.')

        return data

    def create(self, validated_data):
        '''
        Create a new user.
        '''
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        # Hash password
        user.set_password(validated_data['password'])
        user.save()

        # Create a UserProfile when a new user is created
        # and assign it to the newly created user
        UserProfile.objects.create(user=user)

        return user

    def update(self, instance, validated_data):
        '''
        Update the user.
        '''
        # Update the username
        if validated_data.get('username'):
            instance.username = validated_data.get('username')

        # Update the email address
        if validated_data.get('email'):
            instance.email = validated_data.get('email')

        # Update the password
        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))

        instance.save()

        return instance
