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
            max_size:
                max file size in bytes
        '''
        self.max_size = max_size

    def __call__(self, value: int):
        if value.size > self.max_size:
            raise ValidationError(
                'Please upload a file size <= {0:.2f}MB'.format(
                    self.max_size/(1<<20)
                )
            )