# Generated by Django 4.2.3 on 2023-09-21 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dailyreport', '0007_inflowsdischarge'),
    ]

    operations = [
        migrations.AddField(
            model_name='inflowsdischarge',
            name='InfDis00to24',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='inflowsdischarge',
            name='InfDis06to06',
            field=models.IntegerField(default=0),
        ),
    ]
