from django.urls import path

from simulation import views

urlpatterns = [
    path('', views.SimulationCreate.as_view()),
    path('bike/', views.AreaView.as_view()),
    path('packages/', views.PackageView.as_view()),
    path('lockers/', views.LockerView.as_view()),
]
