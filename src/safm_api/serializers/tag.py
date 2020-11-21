from rest_framework import serializers
from safm_api.models import Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        app_label = 'safm_api'
        model = Tag
        fields = '__all__'
