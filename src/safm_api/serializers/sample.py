import re
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

        # Parse the tags and assign them to the sample
        sample.set_tags(self.parse_tags(**validated_data['tags']))

        # Parse the forks and assign them to the sample
        sample.set_forks(self.parse_forks(**validated_data['forks_from']))

        return sample

    def update(self, instance, validated_data):
        '''
        Update the sample.
        '''
        # Clear the tags
        instance.tags.clear()
        # Parse the tags and assign them to the sample
        instance.set_tags(self.parse_tags(**validated_data['tags']))

        # Clear the forks
        instance.forks.clear()
        # Parse the forks and assign them to the sample
        instance.set_forks(self.parse_forks(**validated_data['forks_from']))

        instance.save()

        return instance

    def validate_file(self, value):
        '''
        Make sure that the filename does not contain
        characters that are invalid.
        '''
        value.name = get_safe_file_name(value.name)
        return value

    def parse_tags(self, tags):
        '''
        Parse the received tags (string separated by commas).
        '''
        tags_as_string = re.escape(tags).replace('\\', '')

        # Filter the valid tags
        tags_as_list = list(filter(re.compile(r'[a-z]+[a-z0-9]+'),
                                   [tag.strip() for tag in tags_as_string.split(',')]
                                   ))

        return tags_as_list

    def parse_forks(self, forks):
        '''
        Parse the received forks (string separated by commas).
        '''
        forks_as_string = re.escape(forks).replace('\\', '')

        # Filter the valid forks
        forks_as_list = list(filter(re.compile(r'\d'),
                                    [fork.strip() for fork in forks_as_string.split(',')]
                                    ))

        return forks_as_list
