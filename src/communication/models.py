from django.db import models


class Instance(models.Model):
    company = models.ForeignKey("rest_api.Company", on_delete=models.CASCADE)
    instance_url = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
