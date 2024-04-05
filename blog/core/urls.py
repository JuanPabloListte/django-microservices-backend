from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("api/posts/", include('apps.posts.urls')),
    path("api/cateogry/", include('apps.category.urls')),
    path('admin/', admin.site.urls),
]
