# Generated by Django 5.2.3 on 2025-07-14 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upcoming_list', '0002_upcomingdata_last_accessed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='upcomingdata',
            name='last_accessed',
        ),
    ]
