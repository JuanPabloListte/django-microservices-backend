from .views import *
from django.urls import path, include

urlpatterns = [
    path("list/", ListPostView.as_view()),
    path("get/<id>/", DetailPostView.as_view()),
    path("create/", CreatePostView.as_view()),
    path("update/", UpdatePostView.as_view()),
    path("delete/<id>", DeletePostView.as_view())
]
