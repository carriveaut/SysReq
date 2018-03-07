from django.contrib.auth.models import Group
from django.db import models
#from Tickets import models

# Create your models here.
#from Tickets.models import Ticket


class Cart(models.Model):
    ticketID = models.ForeignKey('Tickets.Ticket', on_delete=models.CASCADE)
    id = models.ForeignKey(Group)
    cartQty = models.BigIntegerField
    cartPrice = models.FloatField
    cartDate = models.DateTimeField