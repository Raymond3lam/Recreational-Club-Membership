from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

class CustomUserAdmin(UserAdmin):
    model = models.CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('practices',)}),
    )

# Register your models here.
admin.site.register(models.Announcement)
admin.site.register(models.CustomUser, CustomUserAdmin)
admin.site.register(models.Practice)