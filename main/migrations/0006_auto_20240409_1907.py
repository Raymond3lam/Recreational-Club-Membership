# Generated by Django 5.0.3 on 2024-04-09 23:07

from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from main.models import CustomUser, Practice, Announcement

def create_groups(apps, schema_editor):
    members_group, created = Group.objects.get_or_create(name='Members')
    coaches_group, created = Group.objects.get_or_create(name='Coaches')

    content_type_practice = ContentType.objects.get_for_model(Practice)
    content_type_announcement = ContentType.objects.get_for_model(Announcement)
    members_group.permissions.add(
        Permission.objects.get(content_type=content_type_practice, codename='view_practice'),
        Permission.objects.get(content_type=content_type_announcement, codename='view_announcement'),
    )
    coaches_group.permissions.add(
        Permission.objects.get(content_type=content_type_practice, codename='view_practice'),
        Permission.objects.get(content_type=content_type_practice, codename='add_practice'),
        Permission.objects.get(content_type=content_type_practice, codename='change_practice'),
        Permission.objects.get(content_type=content_type_practice, codename='delete_practice'),
        Permission.objects.get(content_type=content_type_announcement, codename='view_announcement'),
        Permission.objects.get(content_type=content_type_announcement, codename='add_announcement'),
        Permission.objects.get(content_type=content_type_announcement, codename='change_announcement'),
        Permission.objects.get(content_type=content_type_announcement, codename='delete_announcement'),
    )

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20240409_1838'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
