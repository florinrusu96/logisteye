from django.db import models


class CourierToPackage(models.Model):
    package = models.ForeignKey("Package", on_delete=models.CASCADE)
    courier = models.ForeignKey("User", on_delete=models.CASCADE)
    pickup_location = models.ForeignKey("Location", on_delete=models.CASCADE)
    drop_off_location = models.ForeignKey("Location", on_delete=models.CASCADE,
                                          related_name="drop_off_location_location")

