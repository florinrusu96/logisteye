from django.conf.urls import url
from simulation import views

urlpatterns = [
    url('insert-simulation-data/', views.SimulationCreate.as_view()),
]
