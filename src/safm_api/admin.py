from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Tag)
admin.site.register(Sample)
admin.site.register(UserProfile)
admin.site.register(UserSampleDownload)
