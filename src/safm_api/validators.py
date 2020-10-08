import tempfile

import audiofile as af
from django.conf import settings
from rest_framework.serializers import ValidationError


class FileSizeValidator:
    '''
    Validate file size is less than provided value
    Applicable to serializers.FileField
    '''
    def __init__(self, max_size: int=settings.MAX_FILE_UPLOAD_SIZE):
        '''
        Params:
        ---------
            max_size:  max file size in bytes
        '''
        self.max_size = max_size

    def __call__(self, value):
        if value.size > self.max_size:
            raise ValidationError(
                'Please upload a file with size <= {0:.2f}MB'.format(
                    self.max_size/(1<<20)
                )
            )

class AudioFileDurationValidator:
    '''
    Validate audio file duration to be less than provided value
    Applicable to audio files
    '''

    def __init__(self, max_duration: float=settings.MAX_AUDIO_DURATION):
        '''
        Params:
        --------
            max_duration: max duration in seconds
        '''
        self.max_duration = max_duration

    def __call__(self, value):
        # in order for duration to be calculated, file must be
        # temporarily written to disk
        with tempfile.NamedTemporaryFile() as tmp_file:
            for chunk in value.chunks():
                tmp_file.write(chunk)

            duration = af.duration(tmp_file.name)
            print(f"Duration is {duration:.2f}")
            if duration > self.max_duration:
                raise ValidationError(
                    'Please upload a sample <= {0:.1f}s'.format(
                        self.max_duration
                    )
                )
