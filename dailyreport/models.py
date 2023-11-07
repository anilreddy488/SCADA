from email.policy import default
from multiprocessing import Value
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime



class GeneratingStation(models.Model):
    GenStationName = models.CharField(unique=True,max_length=100)
    GenType = models.CharField(max_length=100)
    InstalledCap = models.FloatField()
    GenStationID = models.AutoField(primary_key=True)

    def __str__(self):
        return self.GenStationName


class GridFreq(models.Model):
    FreqMorning = models.FloatField()
    FreqEvening = models.FloatField()
    TimeMaxDemandMorning = models.TimeField()
    TimeMaxDemandEvening = models.TimeField()
    Date = models.DateField(unique=True,default=datetime.date.today)

    def __str__(self):
        return self.GenStationName

class DemandData(models.Model):
    GenStationID = models.IntegerField()
    GenStationName = models.CharField(default='abc',max_length=100)
    GenType = models.CharField(default='abc',max_length=100)
    InstalledCap = models.FloatField(default=0)
    MorningPeak = models.FloatField()
    EveningPeak = models.FloatField()
    Energy = models.FloatField()
    Date = models.DateField(default=datetime.date.today)
    class Meta:
        unique_together = (('Date', 'GenStationID'),)

    def __str__(self):
        return f"DemandData - {self.Date}"


class MaxCitySolar(models.Model):
    PID = models.IntegerField()
    Name = models.CharField(max_length=100)
    MaxDemand = models.FloatField()
    Time = models.TimeField()
    Date = models.DateField(default=datetime.date.today)
    class Meta:
        unique_together = (('Date', 'PID'),)

    def __str__(self):
        return f"MaxDemandCityandSolar - {self.Date}"

class SchDrwlData(models.Model):
    StateID = models.IntegerField()
    StateName = models.CharField(default="",max_length=30)
    Schedule = models.FloatField()
    Drawl = models.FloatField()
    Date = models.DateField(default=datetime.date.today)
    class Meta:
        unique_together = (('Date', 'StateID'),)

    def __str__(self):
        return f"SchDrwlData - {self.Date}"

class CentralSectorData(models.Model):
    CentralStationID = models.IntegerField()
    CenStationName = models.CharField(default="",max_length=30)
    Energy = models.FloatField()
    Date = models.DateField(default=datetime.date.today)
    class Meta:
        unique_together = (('Date', 'CentralStationID'),)

    def __str__(self):
        return f"CentralSectorData - {self.Date}"

class LevelStorage(models.Model):
    DamID = models.IntegerField()
    Level = models.FloatField()
    Storage = models.FloatField()

    def __str__(self):
        return f"LevelStorage - {self.Date}"

class LevelStorageData(models.Model):
    DamID = models.IntegerField()
    DamName = models.CharField(default="",max_length=30)
    Level = models.FloatField()
    Date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"LevelStorageData - {self.Date}"

class InflowsDischarge(models.Model):
    ReservoirID = models.IntegerField()
    Name = models.CharField(default="",max_length=30)
    Type = models.CharField(default="",max_length=30)
    DamName = models.CharField(default="",max_length=30)
    InfDis00to24 = models.IntegerField(default=0)
    InfDis06to06 = models.IntegerField(default=0)
    Date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"InflowsDischarge - {self.Date}"

class WeatherandOtherParameters(models.Model):
    WID = models.IntegerField()
    Name = models.CharField(default="",max_length=30)
    Type = models.CharField(default="",max_length=30)
    Value = models.CharField(default="",max_length=30)
    Date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"WeatherandOtherParameters - {self.Date}"

class CoalParticulars(models.Model):
    GenStationID = models.IntegerField()
    GenStationName = models.CharField(default="",max_length=30)
    OpenBal = models.IntegerField()
    Receipts = models.IntegerField()
    Consumption = models.IntegerField()
    AvgCoalperDay = models.IntegerField()
    Date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"CoalParticulars - {self.Date}"

class WagonParticulars(models.Model):
    GenStationID = models.IntegerField()
    GenStationName = models.CharField(default="",max_length=30)
    OpenBal = models.IntegerField()
    Receipts = models.IntegerField()
    Tippled = models.IntegerField()
    Pending = models.IntegerField()
    Date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"WagonParticulars - {self.Date}"
