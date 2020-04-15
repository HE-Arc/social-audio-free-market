from django.db import models
from django.contrib.auth.models import User

import os

# Create your models here.

class Sample(models.Model):
    # Audio Sample

    class Tone(models.TextChoices):
        # Tone Enum
        A = 'A'
        B = 'B'
        C = 'C'
        D = 'D'
        E = 'E'
        F = 'F'
        G = 'G'

    class Mode(models.TextChoices):
        # Mode Enum
        MINOR = 'm', 'Minor'
        MAJOR = 'M', 'Major'

    def user_directory_path(instance, filename):
        # File will be uploaded to MEDIA_ROOT/samples/<username>/<sample_name>
        ext = os.path.splitext(filename)[1]
        return 'samples/{0}/{1}{2}'.format(instance.user.username, instance.name, ext)

    # Table columns
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    file = models.FileField(max_length=255, upload_to=user_directory_path)
    duration = models.FloatField(blank=True, null=True) # duration in [s]
    tempo = models.PositiveIntegerField(blank=True, null=True) # tempo is > 0
    tone = models.CharField(max_length=1, choices=Tone.choices, blank=True)
    mode = models.CharField(max_length=1, choices=Mode.choices, blank=True)
    datetime_upload = models.DateTimeField(auto_now_add=True) # auto now at creation
    nb_dl_unauthenticated = models.PositiveIntegerField(default=0) # nb dl > 0
