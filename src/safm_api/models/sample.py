from django.db import models

from .tag import Tag
from django.contrib.auth.models import User

from safm_api.utils import get_safe_file_name, get_file_bpm
import audiofile as af


class Sample(models.Model):

    class Meta:
        app_label = 'safm_api'

    class Key(models.TextChoices):
        # Key Enum
        NONE = ' '
        A = 'A'
        B = 'B'
        C = 'C'
        D = 'D'
        E = 'E'
        F = 'F'
        G = 'G'

    class Mode(models.TextChoices):
        # Mode Enum
        NONE = ' '
        MINOR = 'min'
        MAJOR = 'maj'

    def sample_path(instance, filename):
        '''
        Returns the sample file path.
        '''
        filename = get_safe_file_name(filename)
        return 'samples/{0}/{1}'.format(instance.user.id, filename)

    # Table columns
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50)
    file = models.FileField(max_length=255, upload_to=sample_path)
    # duration in [s]
    duration = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        blank=True,
        null=True
    )
    # tempo is > 0
    tempo = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    key = models.CharField(
        max_length=1,
        choices=Key.choices,
        blank=True,
        default=Key.NONE
    )
    mode = models.CharField(
        max_length=3,
        choices=Mode.choices,
        blank=True,
        default=Mode.NONE
    )
    description = models.TextField(
        blank=True,
        default='No description provided.'
    )
    datetime_upload = models.DateTimeField(
        auto_now_add=True  # auto now at creation
    )
    number_downloads = models.PositiveIntegerField(default=0)  # nb dl > 0
    tags = models.ManyToManyField(Tag)  # a sample can have multiple tags
    forks = models.ManyToManyField(
        'self',
        related_name='forks_to',
        symmetrical=False
    )

    def deduce_properties(self):
        '''
        Deduces the sample duration and tempo.
        '''
        # Duration
        self.duration = af.duration(self.file.path)

        # Sampling rate
        self.tempo = get_file_bpm(self.file.path)

        self.save()
