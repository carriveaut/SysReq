from django.db import models
import datetime

# Create your models here.


class Ticket(models.Model):
    event = models.CharField(max_length=100)
    venue_Name = models.CharField(max_length=100)
    venue_Info = models.CharField(max_length=150)
    start_Date = models.DateField(default=datetime.date.today)
    start_Time = models.TimeField(default=datetime.time(16, 00), null=True)
    price = models.DecimalField(default=89.99, max_digits=9, decimal_places=2)
    status = models.CharField(max_length=25)
    qty = models.IntegerField(default=50)
    classification = models.CharField(max_length=100)
    image_Url = models.CharField(default="/static/Home/images/no-image.jpg", max_length=250)
    # ticketID = models.AutoField(primary_key=True)
    # ticketName = models.CharField(max_length=50)
    # ticketDesc = models.CharField(max_length=250)
    # ticketType = models.CharField(max_length=50)
    # ticketDateTime = models.DateTimeField
    # ticketVenue = models.CharField(max_length=100)
    # ticketAddress = models.CharField(max_length=100)
    # ticketCity = models.CharField(max_length=50)
    # ticketState = models.CharField(max_length=2)
    # ticketZip = models.CharField(max_length=10)
    # ticketPrice = models.DecimalField
    # ticketImage = models.ImageField