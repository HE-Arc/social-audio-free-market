from rest_framework import serializers
from safm_api.utils import get_safe_file_name
from safm_api.validators import FileSizeValidator, AudioFileDurationValidator
from safm_api.models.sample import Sample


class SampleForkSerializer(serializers.ModelSerializer):
    file = serializers.FileField(validators=[
        FileSizeValidator(),
        AudioFileDurationValidator(),
    ])

    class Meta:
        app_label = 'safm_api'
        model = Sample
        fields = '__all__'

    def validate_file(self, value):
        '''
        Make sure that the filename does not contain
        characters that are invalid.
        '''
        value.name = get_safe_file_name(value.name)
        return value
