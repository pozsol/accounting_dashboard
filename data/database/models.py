from django.db import models
from manage import init_django


init_django()


class Patient(models.Model):
    name = models.CharField(max_length=100)


class Department(models.Model):
    name = models.CharField(max_length=100)


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL())


class Type(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()


class Device(models.Model):
    name = models.CharField()


class Examination(models.Model):
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL())
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL())
    type = models.ForeignKey(Type, on_delete=models.SET_NULL())
    device = models.ForeignKey(Device, on_delete=models.SET_NULL())
