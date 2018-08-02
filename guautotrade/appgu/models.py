from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
import datetime


class Dealers(models.Model):
    class Meta:
        verbose_name_plural = "Dealers"

    dealerID = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    telephone = models.CharField(max_length=12)
    isBlocked = models.BooleanField(default=False)


class Orders(models.Model):
    class Meta:
        verbose_name_plural = "Orders"

    dealerID = models.ForeignKey(Dealers, db_column='dealerID', on_delete=models.CASCADE)
    model = models.CharField(max_length=1000)
    colour = models.CharField(max_length=1000)
    date = models.DateField(auto_now_add=True)
    homologation = models.BooleanField(default=False)
    custom_clearance = models.BooleanField(default=False)
    additional_comments = models.CharField(max_length=1000)

    scheduled_completion_date = models.CharField(max_length=100)
    deposit_received = models.BooleanField(default=False)
    payment_received = models.BooleanField(default=False)
    invoice = models.FileField(upload_to='portal_invoices/', blank=True, null=True)


class Vehicles(models.Model):
    model = models.CharField(max_length=1000)
    headline = models.CharField(max_length=1000)
    description = models.CharField(max_length=5000)
    image = models.ImageField(default='default_vehicle.png', upload_to='vehicles/', blank=True, null=True)

class NewsPosts(models.Model):
    writtenby = models.ForeignKey(User, db_column='dealerID', on_delete=models.CASCADE)
    banner = models.ImageField(default='default_banner.png', upload_to='news/banners/', blank=True, null=True)
    title = models.CharField(max_length=1000)
    headline = models.CharField(max_length=1000)
    description = models.CharField(max_length=5000)
    quote = models.CharField(max_length=1000)
    quotefooter = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=True)

class Events(models.Model):
    title = models.CharField(max_length=1000)
    description = models.CharField(max_length=5000)
    link = models.CharField(max_length=1000)
    date = models.DateField()

class MapDealers(models.Model):
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=70, blank=True, null=True, unique=True)
    address = models.CharField(max_length=500)
    country = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
