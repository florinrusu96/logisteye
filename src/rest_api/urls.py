from django.conf.urls import url
from rest_api import views

urlpatterns = [
    url("packages/", views.PackageListView.as_view()),

]
