from django.db import models


class Package(models.Model):
    source_location = models.ForeignKey("Location", on_delete=models.CASCADE)
    destination_location = models.ForeignKey("Location", on_delete=models.CASCADE,
                                             related_name="destination_location_location")
    current_location = models.ForeignKey("Location", on_delete=models.CASCADE,
                                         related_name="current_location_location")
    company = models.ForeignKey("Company", on_delete=models.CASCADE)
    is_delivered = models.BooleanField()
    date = models.DateField(auto_now=True)
