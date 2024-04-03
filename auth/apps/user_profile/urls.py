from django.urls import path
from .views import *

urlpatterns = [
    path("get/profile/<id>/", GetUserProfileView.as_view()),
    path("my_profile/", MyUserProfileView.as_view()),
    path("edit/username", EditUsernameView.as_view())
]
