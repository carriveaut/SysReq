from django.db import models
import datetime
from decimal import Decimal

from payments import PurchasedItem
from payments.models import BasePayment


class Payment(BasePayment):

    def get_failure_url(self):
        return 'http://example.com/failure/'

    def get_success_url(self):
        return 'http://example.com/success/'

    def get_purchased_items(self):
        # you'll probably want to retrieve these from an associated order
        yield PurchasedItem(name='The Hound of the Baskervilles', sku='BSKV',
                            quantity=9, price=Decimal(10), currency='USD')


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


class Checkout(models.Model):
    NameOnCard = models.CharField(max_length=50)
    CCN = models.CharField(max_length=16)
    CCED = models.DateField
    CCCVV = models.CharField(max_length=16)
    BAddress = models.CharField(max_length=250)
    BCity = models.CharField(max_length=25)
    BState = models.CharField(max_length=2)
    BZip = models.CharField(max_length=5)
    ShipName = models.CharField(max_length=50)
    ShipAddress = models.CharField(max_length=250)
    ShipCity = models.CharField(max_length=25)
    ShipState = models.CharField(max_length=2)
    ShipZip = models.CharField(max_length=5)
