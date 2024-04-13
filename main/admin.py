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

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted', 'date_updated')
    list_filter = ('author', 'date_posted')
    search_fields = ('title', 'content')
    filter_horizontal = ('target', 'target_practices')

# Register your models here.
admin.site.register(models.Announcement, AnnouncementAdmin)
admin.site.register(models.CustomUser, CustomUserAdmin)
admin.site.register(models.Practice, PracticeAdmin)
admin.site.register(models.Payment, PaymentAdmin)
admin.site.register(models.Expense)