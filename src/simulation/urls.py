from django.conf.urls import url
from simulation import views

urlpatterns = [
    url('', views.SimulationCreate.as_view()),
]
