from django.contrib import admin

# Register your models here.
from communication import models

admin.site.register(models.Instance)