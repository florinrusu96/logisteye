from rest_api import models


def generate_couriers(count):
    for i in range(count):
        dict = {
            'email': f'email{i}@email.com',
            'first_name': f'first_name{i}',
            'last_name': f'last_name{i}',
            'password': 'p@ssw0rd',
        }
        models.User.objects.create(**dict)
