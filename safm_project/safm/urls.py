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
    
    path('api/forks/from/<int:sample_id>', ListSampleForkFrom.as_view()),
    path('api/forks/to/<int:sample_id>', ListSampleForkTo.as_view()),

    path('api/user/downloads', UserDownloads.as_view()),
    path('api/user/samples/<int:user_id>', UserSamples.as_view()),
    path('api/user/samples/count/<int:user_id>', UserSamplesCount.as_view()),
    path('api/user/profile/<int:id>', UserProfileView.as_view()),
    path('api/user/picture/<int:user_id>', UserProfilePicture.as_view()),
    path('api/user/email/<int:user_id>', UserEmail.as_view()),
]
