from django.db import models

# Create your models here.

class Ticket(models.Model):
    ticketID = models.AutoField(primary_key=True)
    ticketName = models.CharField(max_length=50)
    ticketDesc = models.CharField(max_length=250)
    ticketType = models.CharField(max_length=50)
    ticketDateTime = models.DateTimeField
    ticketVenue = models.CharField(max_length=100)
    ticketAddress = models.CharField(max_length=100)
    ticketCity = models.CharField(max_length=50)
    ticketState = models.CharField(max_length=2)
    ticketZip = models.CharField(max_length=10)
    ticketPrice = models.DecimalField
    ticketImage = models.ImageField