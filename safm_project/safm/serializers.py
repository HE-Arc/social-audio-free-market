from rest_framework import serializers
from .models import Sample
from .models import Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class SampleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True) # join on tags

    class Meta:
        model = Sample
        fields = '__all__'
