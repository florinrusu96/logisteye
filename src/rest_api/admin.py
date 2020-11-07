from django.contrib import admin
from rest_api import models

# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Area)
admin.site.register(models.CourierToPackage)
admin.site.register(models.Package)
admin.site.register(models.Location)
admin.site.register(models.Size)
admin.site.register(models.Company)
admin.site.register(models.Box)
admin.site.register(models.Locker)
