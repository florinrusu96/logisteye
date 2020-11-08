from rest_framework import generics, response, status

from simulation import serializers
from rest_api.models import User, Package, CourierToPackage, Locker, Location, Size

import os
import random

from simulation.generators.constants import *

os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
import django

django.setup()
from simulation.generators import packages, lockers, couriers
from rest_api import models
from rest_api.routing import routing


class SimulationCreate(generics.CreateAPIView):
    serializer_class = serializers.SimulationSerializer

    def post(self, request, *args, **kwargs):
        User.objects.exclude(is_superuser=True).delete()
        Package.objects.all().delete()
        CourierToPackage.objects.all().delete()
        Locker.objects.all().delete()

        insert_all_data()

        routing.run_routing_algorithm()

        time = routing.compute_time_needed_for_deliveries()
        co2 = routing.compute_saved_co2()

        return response.Response(status=status.HTTP_200_OK, data={"time": time, "co2": co2})


def insert_package_data(company):
    destinations = packages.generate_packages(30, [(48.8718468, 2.3665066), (48.8263230, 2.2876292)])
    source_location = models.Location.objects.create(latitude=PARIS_LOW_LAT, longitude=PARIS_LOW_LONG)
    for d in destinations:
        dest_location = models.Location.objects.create(latitude=d[0], longitude=d[1])

        package = {
            'company': company,
            'source_location': source_location,
            'destination_location': dest_location,
            'is_delivered': False
        }
        Package.objects.create(**package)


def insert_locker(company, locker):
    locker_data = {
        'owner': company,
        'location': Location.objects.create(latitude=locker.lat, longitude=locker.long, name=locker.name),
        'price': 40
    }
    created_locker = models.Locker.objects.create(**locker_data)
    for idx in range(int(random.uniform(17, 35))):
        data = {
            'locker': created_locker,
            'size': Size.objects.get(name='small')
        }
        models.Box.objects.create(**data)


def insert_all_data():
    lockers_list = lockers.generate_lockers(300 * 3)

    company1 = models.Company.objects.get(name='company1')
    insert_package_data(company1)
    for i, locker in zip(range(25), lockers_list[0:25]):
        insert_locker(company1, locker)

    company2 = models.Company.objects.get(name='company2')
    insert_package_data(company2)
    for i, locker in zip(range(25), lockers_list[25:50]):
        insert_locker(company2, locker)

    company3 = models.Company.objects.get(name='company3')
    insert_package_data(company3)
    for i, locker in zip(range(25), lockers_list[50:75]):
        insert_locker(company3, locker)

    couriers.generate_couriers(30)
