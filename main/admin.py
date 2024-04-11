from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

class PracticeInline(admin.TabularInline):
    model = models.Practice.members.through

class CustomUserAdmin(UserAdmin):
    model = models.CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'address', 'paid')}),
    )
    inlines = [PracticeInline]

class PracticeAdmin(admin.ModelAdmin):
    filter_horizontal = ('members',)

# Register your models here.
admin.site.register(models.Announcement)
admin.site.register(models.CustomUser, CustomUserAdmin)
admin.site.register(models.Practice, PracticeAdmin)
admin.site.register(models.Payment)