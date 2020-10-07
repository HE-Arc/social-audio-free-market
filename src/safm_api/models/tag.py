from django.db import models

import os

class Tag(models.Model):

    class Meta:
        app_label = 'safm_api'

    name = models.CharField(max_length=20)
