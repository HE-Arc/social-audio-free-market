from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('api/login', views.Login.as_view()),
    path('api/logout', views.Logout.as_view()),
    path('api/register', views.Register.as_view()),

    # Search
    path('api/search/quick', views.QuickSearch.as_view()),
    path('api/search/advanced', views.AdvancedSearch.as_view()),

    # Sample
    path('api/sample', views.SampleView.as_view()),
    path('api/sample/<int:pk>', views.SampleView.as_view()),
    path('api/sample/file/<int:pk>/<int:download>', views.SampleFile.as_view()),
    path('api/sample/like/<int:pk>', views.SampleLikeView.as_view()),
    path('api/samples/last', views.ListLastUploadedSamples.as_view()),

    # Sample fork
    path('api/forks/from/<int:pk>', views.ListSampleForkFrom.as_view()),
    path('api/forks/to/<int:pk>', views.ListSampleForkTo.as_view()),

    # User
    path('api/user/<int:pk>', views.UserUpdate.as_view()),
    path('api/user/profile/<int:pk>', views.UserProfileView.as_view()),
    path('api/user/picture/<int:pk>', views.UserProfilePicture.as_view()),
    path('api/user/email/<int:pk>', views. UserEmail.as_view()),
    path('api/user/samples/likes', views.UserSampleLikes.as_view()),
    path('api/user/downloads', views.UserDownloads.as_view()),
    path('api/user/samples/<int:pk>', views.UserSamples.as_view()),
    path('api/user/samples/count/<int:pk>', views.UserSamplesCount.as_view()),
]
