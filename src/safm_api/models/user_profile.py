from django.db import models
from django.conf import settings

from django.contrib.auth.models import User

import os

class UserProfile(models.Model):

    class Meta:
        app_label = 'safm_api'

    def profile_picture_path(instance, filename):
        '''
        Returns the user profile picture file path.
        '''
        ext = os.path.splitext(filename)[1]
        return 'users/{0}/pp{1}'.format(instance.user.id, ext)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, default='No description provided.')
    profile_picture = models.FileField(max_length=255, upload_to=profile_picture_path, blank=True, default=settings.DEFAULT_PROFILE_PICTURE)
    email_public = models.BooleanField(default=False)

    @property
    def has_default_picture(self):
        return self.profile_picture.name == settings.DEFAULT_PROFILE_PICTURE
