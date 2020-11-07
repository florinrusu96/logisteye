from django.conf.urls import url
from django.urls import path
from rest_api import views

urlpatterns = [
    url("packages/", views.PackageListView.as_view()),
    path("users/", views.UserPostView.as_view())
]
