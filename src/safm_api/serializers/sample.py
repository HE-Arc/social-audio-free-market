from rest_framework import serializers
from .sample_fork import SampleForkSerializer
from .tag import TagSerializer
from .user import UserSerializer
from safm_api.utils import get_safe_file_name
from safm_api.validators import FileSizeValidator, AudioFileDurationValidator
from safm_api.models.sample import Sample


class SampleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tags = TagSerializer(
        many=True,
        required=False
    )
    forks = SampleForkSerializer(
        write_only=True,
        many=True,
        required=False
    )
    file = serializers.FileField(validators=[
        FileSizeValidator(),
        AudioFileDurationValidator(),
    ])

    class Meta:
        app_label = 'safm_api'
        model = Sample
        fields = '__all__'

    def create(self, validated_data):
        '''
        Create a new sample.
        '''
        sample = Sample.objects.create(**validated_data)

        # Automatically deduce some properties
        sample.deduce_properties()
        sample.save()

        return sample

    def validate_file(self, value):
        '''
        Make sure that the filename does not contain
        characters that are invalid.
        '''
        value.name = get_safe_file_name(value.name)
        return value
