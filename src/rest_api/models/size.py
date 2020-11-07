from django.db import models


class Size(models.Model):
    width = models.FloatField(help_text="centimeters")
    height = models.FloatField(help_text="centimeters")
    depth = models.FloatField(help_text="centimeters")
    name = models.CharField(max_length=120, null=True)