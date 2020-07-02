from django.urls import path
from .views import *

urlpatterns = [
    path('api/login', Login.as_view()),
    path('api/logout', Logout.as_view()),
    path('api/register', Register.as_view()),
    
    path('api/quick', QuickSearch.as_view()),
    path('api/ad_search', AdvancedSearch.as_view()),

    path('api/sample', SampleView.as_view()),
    path('api/sample/<int:id>', SampleView.as_view()),
    path('api/sample/file/<int:sample_id>/<int:download>', SampleFile.as_view()),
    path('api/samples/<int:user_id>', UserSamples.as_view()),
    
    path('api/sample/forks/from/<int:sample_id>', ListSampleForkFrom.as_view()),
    path('api/sample/forks/to/<int:sample_id>', ListSampleForkTo.as_view()),

    path('api/user_downloads/', UserDownloads.as_view()),
    path('api/profile/<int:user_id>', UserProfilePage.as_view()),
]
