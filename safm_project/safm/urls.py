from django.urls import path
from .views import *

urlpatterns = [
    path('api/quick', QuickSearch.as_view()),
    path('api/download_sample/<int:sample_id>', DownloadSample.as_view()),
]
