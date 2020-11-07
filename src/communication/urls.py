from django.conf.urls import url
from communication import views

urlpatterns = [
    url('packages/', views.PackageForInstanceList.as_view()),
]
