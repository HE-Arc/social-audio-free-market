from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Tag
from .models import Sample

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

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
