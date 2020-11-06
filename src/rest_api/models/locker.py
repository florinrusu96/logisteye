from django.db import models


class Locker(models.Model):
    location = models.OneToOneField("Location", on_delete=models.CASCADE)
    owner = models.OneToOneField("Company", on_delete=models.CASCADE)
    price = models.FloatField(default=1)