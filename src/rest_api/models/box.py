from django.db import models


class Box(models.Model):
    locker = models.ForeignKey("Locker", on_delete=models.CASCADE)
    is_empty = models.BooleanField(default=True)
    size = models.ForeignKey("Size", on_delete=models.CASCADE)

