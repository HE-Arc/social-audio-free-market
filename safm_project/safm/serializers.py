from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class SampleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False) # Join on tags
    user = UserSerializer(required=False) # Not required in order to set the current user

    class Meta:
        model = Sample
        fields = '__all__'


class UserDownloadSerializer(serializers.ModelSerializer):
    sample = SampleSerializer()

    class Meta:
        model = UserSampleDownload
        fields = '__all__'


class SampleForkFromSerializer(serializers.ModelSerializer):
    sample_from = SampleSerializer()

    class Meta:
        model = SampleForkFrom
        fields = ['sample_from']


class SampleForkToSerializer(serializers.ModelSerializer):
    sample_to = SampleSerializer()

    class Meta:
        model = SampleForkTo
        fields = ['sample_to']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = '__all__'
