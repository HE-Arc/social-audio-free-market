from rest_framework import serializers
from .sample import SampleSerializer
from safm_api.models import SampleLike


class SampleLikeSerializer(serializers.ModelSerializer):
    sample = SampleSerializer()

    class Meta:
        app_label = 'safm_api'
        model = SampleLike
        fields = ['sample', 'datetime_like']
