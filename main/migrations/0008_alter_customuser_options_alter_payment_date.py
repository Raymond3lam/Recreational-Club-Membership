# Generated by Django 5.0.3 on 2024-04-11 23:39

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_remove_customuser_paid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'permissions': [('manage_coaches', 'Can manage coaches'), ('manage_finances', 'Can manage finances')]},
        ),
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
