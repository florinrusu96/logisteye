from django.db import models


class Area(models.Model):
    location_center = models.OneToOneField("Location", on_delete=models.CASCADE)
    radius = models.FloatField()
