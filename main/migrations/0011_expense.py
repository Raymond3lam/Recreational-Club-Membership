# Generated by Django 5.0.3 on 2024-04-13 00:40

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_announcement_target_practices'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('paid', models.BooleanField(default=False)),
                ('due', models.DateTimeField(default=django.utils.timezone.now)),
                ('notes', models.TextField()),
                ('category', models.CharField(max_length=100)),
            ],
        ),
    ]