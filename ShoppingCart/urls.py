from django.urls import path

from . import views
app_name = 'ShoppingCart'

urlpatterns = [
    path('', views.shoppingcart, 'shoppingcart'),
]
