from django.urls import path
from .views import *

urlpatterns = [
    path('api/quick', QuickSearch.as_view()),
]
