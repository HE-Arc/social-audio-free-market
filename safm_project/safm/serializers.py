from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    #email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

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
        fields = ['id', 'username', 'email', 'password']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class SampleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True) # join on tags
    user = UserSerializer()

    class Meta:
        model = Sample
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = '__all__'
