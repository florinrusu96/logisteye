import os
import random

from simulation.generators.constants import *

os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
import django

django.setup()
from simulation.generators import packages, lockers, couriers
from rest_api import models
from rest_api.routing import routing


for name in ['company1', 'company2', 'company3']:
    models.Company.objects.create(name=name)


small_size = models.Size.objects.create(width=15, height=15, depth=15, name='small')
medium_size = models.Size.objects.create(width=15, height=15, depth=15, name='medium')
large_size = models.Size.objects.create(width=15, height=15, depth=15, name='large')

sizes = [small_size, medium_size, large_size]


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
        models.Package.objects.create(**package)


def insert_locker(company, locker):
    locker_data = {
        'owner': company,
        'location': models.Location.objects.create(latitude=locker.lat, longitude=locker.long, name=locker.name),
        'price': 40
    }
    created_locker = models.Locker.objects.create(**locker_data)
    for idx in range(int(random.uniform(17, 35))):
        data = {
            'locker': created_locker,
            'size': sizes[int(random.uniform(0, 3))]
        }
        models.Box.objects.create(**data)


lockers_list = lockers.generate_lockers(75 * 3)

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

couriers.generate_couriers(300)

routing.run_routing_algorithm()

print(f"Time needed for deliveries: {routing.compute_time_needed_for_deliveries()}")
