from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

class PracticeInline(admin.TabularInline):
    model = models.Practice.members.through

class CustomUserAdmin(UserAdmin):
    model = models.CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'address')}),
    )
    inlines = [PracticeInline]

class PracticeAdmin(admin.ModelAdmin):
    list_display = ('name', 'coach', 'date')
    filter_horizontal = ('members',)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'date', 'practice')
    list_filter = ('user', 'date')
    search_fields = ('user__username', 'practice__name')

# Register your models here.
admin.site.register(models.Announcement)
admin.site.register(models.CustomUser, CustomUserAdmin)
admin.site.register(models.Practice, PracticeAdmin)
admin.site.register(models.Payment, PaymentAdmin)