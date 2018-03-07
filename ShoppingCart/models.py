from django.db import models
# from Tickets import models

# Create your models here.
class Cart(models.Model):
    cartID = models.AutoField(primary_key=True)
    ticketID = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    qty = models.BigIntegerField
    price = models.FloatField
    name = models.CharField(max_length=50)
    date = models.DateTimeField
    desc = models.CharField(max_length=250)
    img = models.ImageField
