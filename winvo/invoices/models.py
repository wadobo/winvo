from django.db import models

class Year(models.Model):
    name = models.CharField(max_length=10)


class Company(models.Model):
    name = models.CharField(max_length=10)
    cif = models.CharField(max_length=63)
    address = models.CharField(max_length=255)


class Project(models.Model):
    company = models.ForeignKey(Company)
    name = models.CharField(max_length=255)
    currency = models.CharField(max_length=255)
    tax = models.FloatField()
    taxname = models.CharField(max_length=31)


class Invoice(models.Model):
    year = models.ForeignKey(Year)
    num = models.IntegerField(editable=False)


class Fee(models.Model):
    invoice = models.ForeignKey(Invoice)
    summary = models.CharField(max_length=1023)
    fee = models.FloatField()
    hours = models.FloatField(blank=True, null=True)
