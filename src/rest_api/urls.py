from django.conf.urls import url
from django.urls import path
from rest_api import views

urlpatterns = [
    url("packages/", views.PackageListView.as_view()),
    path("users/<int:pk>/", views.UserGetView.as_view())
]
