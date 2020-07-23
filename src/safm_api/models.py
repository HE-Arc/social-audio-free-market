from django.db import models
from django.contrib.auth.models import User

import os, unicodedata
import audiofile as af
import numpy as np
from aubio import source, tempo

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=100)


class Sample(models.Model):
    # Audio Sample

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

    def user_directory_path(instance, filename):
        # File will be uploaded to MEDIA_ROOT/samples/<username>/<filename>
        filename = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore')
        ext = os.path.splitext(filename)[1]
        return 'samples/{0}/{1}{2}'.format(instance.user.id, filename, ext)

    # Table columns
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    file = models.FileField(max_length=255, upload_to=user_directory_path)
    duration = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True) # duration in [s]
    tempo = models.PositiveIntegerField(blank=True, null=True) # tempo is > 0
    key = models.CharField(max_length=1, choices=Key.choices, blank=True, default=Key.NONE)
    mode = models.CharField(max_length=3, choices=Mode.choices, blank=True, default=Mode.NONE)
    description = models.TextField(blank=True, default='No description provided.')
    datetime_upload = models.DateTimeField(auto_now_add=True) # auto now at creation
    number_downloads = models.PositiveIntegerField(default=0) # nb dl > 0
    tags = models.ManyToManyField(Tag) # a sample can have multiple tags
    forks = models.ManyToManyField('self', related_name='forks_to', symmetrical=False)

    def deduce_properties(self):
        # Audio file duration
        self.duration = af.duration(self.file.path)
        
        # Audio file sampling rate
        rate = af.sampling_rate(self.file.path)
        self._deduce_tempo(rate)

        self.save()

    def _deduce_tempo(self, rate):
        win_s, hop_s = 1024, 512
        s = source(self.file.path, rate, hop_s)
        o = tempo('specdiff', win_s, hop_s, rate)
        # List of beats, in samples
        beats = []

        while True:
            samples, read = s()
            is_beat = o(samples)
            if is_beat:
                this_beat = o.get_last_s()
                beats.append(this_beat)
            if read < hop_s:
                break

        if len(beats) > 1:
            self.tempo = np.mean(60. / np.diff(beats))
        else:
            self.tempo = 0
            

class UserProfile(models.Model):
    
    def user_directory_path(instance, filename):
        ext = os.path.splitext(filename)[1]
        return 'users/{0}/pp{1}'.format(instance.user.id, ext)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, default='No description provided.')
    profile_picture = models.FileField(max_length=255, upload_to=user_directory_path, blank=True, default='default/pictures/pp.png')
    email_public = models.BooleanField(default=False)


class UserSampleDownload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    datetime_download = models.DateTimeField(auto_now_add=True) # auto now at creation


class SampleLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    datetime_like = models.DateTimeField(auto_now_add=True) # auto now at creation
