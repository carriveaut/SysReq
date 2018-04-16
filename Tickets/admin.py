from django.contrib import admin

from .models import Ticket, Order, OrderDetail, Checkout
# Register your models here.
admin.site.register(Ticket)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Checkout)
