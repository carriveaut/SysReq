from django.db import models

# Create your models here.


class Ticket(models.Model):
    ticketID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=250)
