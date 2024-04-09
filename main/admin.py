from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Announcement)
admin.site.register(models.Coach)
admin.site.register(models.Member)
admin.site.register(models.Practice)