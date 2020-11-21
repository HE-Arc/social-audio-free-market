from rest_framework import serializers
from .sample import SampleSerializer
from safm_api.models import UserSampleDownload


class UserDownloadSerializer(serializers.ModelSerializer):
    sample = SampleSerializer()

    class Meta:
        app_label = 'safm_api'
        model = UserSampleDownload
        fields = '__all__'
