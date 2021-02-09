from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('api/login', views.LoginView.as_view()),
    path('api/logout', views.LogoutView.as_view()),
    path('api/register', views.RegisterView.as_view()),

    # Search
    path('api/search/quick', views.SampleQuickSearchView.as_view()),
    path('api/search/advanced', views.SampleAdvancedSearchView.as_view()),

    # Sample
    path('api/sample', views.SampleView.as_view()),
    path('api/sample/<int:pk>', views.SampleView.as_view()),
    path('api/sample/file/<int:pk>/<int:download>', views.SampleFileView.as_view()),
    path('api/sample/like/<int:pk>', views.SampleLikeView.as_view()),
    path('api/samples/latest', views.LatestSamplesView.as_view()),

    # Sample fork
    path('api/forks/from/<int:pk>', views.SampleForkFromView.as_view()),
    path('api/forks/to/<int:pk>', views.SampleForkToView.as_view()),

    # User
    path('api/user/<int:pk>', views.UserView.as_view()),
    path('api/user/profile/<int:pk>', views.UserProfileView.as_view()),
    path('api/user/picture/<int:pk>', views.UserProfilePictureView.as_view()),
    path('api/user/email/<int:pk>', views. UserEmailView.as_view()),
    path('api/user/samples/likes', views.UserSampleLikesView.as_view()),
    path('api/user/downloads', views.UserDownloadsView.as_view()),
    path('api/user/samples/<int:pk>', views.UserSamplesView.as_view()),
    path('api/user/samples/count/<int:pk>', views.UserSamplesCountView.as_view()),
]
