from rest_framework import serializers
from .user import UserSerializer
from safm_api.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        app_label = 'safm_api'
        model = UserProfile
        fields = '__all__'
