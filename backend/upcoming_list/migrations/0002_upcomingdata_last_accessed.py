# Generated by Django 5.2.3 on 2025-07-14 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upcoming_list', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='upcomingdata',
            name='last_accessed',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
