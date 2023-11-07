# Generated by Django 4.2.3 on 2023-10-06 11:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dailyreport', '0010_weatherandotherparameters'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoalParticulars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GenStationID', models.IntegerField()),
                ('GenStationName', models.CharField(default='', max_length=30)),
                ('OpenBal', models.IntegerField()),
                ('Receipts', models.IntegerField()),
                ('Consumption', models.IntegerField()),
                ('AvgCoalperDay', models.IntegerField()),
                ('Date', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='WagonParticulars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GenStationID', models.IntegerField()),
                ('GenStationName', models.CharField(default='', max_length=30)),
                ('OpenBal', models.IntegerField()),
                ('Receipts', models.IntegerField()),
                ('Tippled', models.IntegerField()),
                ('Pending', models.IntegerField()),
                ('Date', models.DateField(default=datetime.date.today)),
            ],
        ),
    ]
