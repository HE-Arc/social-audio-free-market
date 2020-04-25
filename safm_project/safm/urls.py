from django.urls import path
from .views import *

urlpatterns = [
    path('api/quick', QuickSearch.as_view()),
    path('api/sample_file/<int:sample_id>', SampleFile.as_view()),
]
