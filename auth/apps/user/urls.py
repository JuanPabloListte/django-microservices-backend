from django.urls import path
from .views import *

urlpatterns = [
    path("list/", ListAllUsersView.as_view()),
    path("get/<id>/", GetUserView.as_view()),
    path("get_details/", GetUserDetailsView.as_view()),
]
