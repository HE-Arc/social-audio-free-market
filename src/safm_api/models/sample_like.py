from django.db import models

from .sample import Sample
from django.contrib.auth.models import User


class SampleLike(models.Model):

    class Meta:
        app_label = 'safm_api'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    datetime_like = models.DateTimeField(
        auto_now_add=True)  # auto now at creation
