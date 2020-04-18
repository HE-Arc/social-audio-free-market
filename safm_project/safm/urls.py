from django.urls import path
from .views import *

urlpatterns = [
    path('quick', QuickSearch.as_view()),
]
