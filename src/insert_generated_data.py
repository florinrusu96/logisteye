import os
import random

os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
import django

django.setup()
from simulation.generators import packages, lockers
from rest_api import models

for name in ['company1', 'company2', 'company3']:
    models.Company.objects.create(name=name)


small_size = models.Size.objects.create(width=15, height=15, depth=15, name='small')
medium_size = models.Size.objects.create(width=15, height=15, depth=15, name='medium')
large_size = models.Size.objects.create(width=15, height=15, depth=15, name='large')

sizes = [small_size, medium_size, large_size]

def insert_package_data(company):
    source_lat, source_long = packages.generate_locations()
    source_location = models.Location.objects.create(latitude=source_lat, longitude=source_long, name='test')
    dest_lat, dest_long = packages.generate_locations()
    dest_location = models.Location.objects.create(latitude=dest_lat, longitude=dest_long, name='test')
    current_lat, current_long = packages.generate_locations()
    current_location = models.Location.objects.create(latitude=current_lat, longitude=current_long, name='test')
    package = {
        'company': company,
        'source_location': source_location,
        'destination_location': dest_location,
        'current_location': current_location,
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
    for idx in range(int(random.uniform(0, 15))):
        data = {
            'locker': created_locker,
            'size': sizes[int(random.uniform(0,3))]
        }
        models.Box.objects.create(**data)


lockers_list = lockers.generate_lockers(75 * 3)

for i, locker in zip(range(25), lockers_list[0:24]):
    company = models.Company.objects.get(name='company1')
    insert_package_data(company)
    insert_locker(company, locker)

for i, locker in zip(range(25), lockers_list[25:49]):
    company = models.Company.objects.get(name='company2')
    insert_package_data(company)

for i, locker in zip(range(25), lockers_list[50:74]):
    company = models.Company.objects.get(name='company3')
    insert_package_data(company)
