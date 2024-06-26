# Generated by Django 4.2.3 on 2023-09-21 07:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dailyreport', '0008_inflowsdischarge_infdis00to24_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LevelStorageData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DamID', models.IntegerField()),
                ('DamName', models.CharField(default='', max_length=30)),
                ('Level', models.FloatField()),
                ('Date', models.DateField(default=datetime.date.today)),
            ],
        ),
    ]
