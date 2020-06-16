from django.urls import path
from rest_framework.authtoken import views
from .views import *

urlpatterns = [
    path('api/login', views.obtain_auth_token),
    path('api/logout', Logout.as_view()),
    path('api/register', Register.as_view()),
    path('api/quick', QuickSearch.as_view()),
    path('api/ad_search', AdvancedSearch.as_view()),
    path('api/sample/<int:sample_id>', SamplePage.as_view()),
    path('api/upload_sample', SampleUpload.as_view()),
    path('api/sample_file/<int:sample_id>/<int:download>', SampleFile.as_view()),
    path('api/profile/<str:username>', UserProfilePage.as_view()),
    path('api/samples/<str:username>', UserSamples.as_view()),
]
