# Generated by Django 4.2.3 on 2023-10-28 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dailyreport', '0013_maxdemandcityandsolar'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MaxDemandCityandSolar',
            new_name='MaxCitySolar',
        ),
    ]