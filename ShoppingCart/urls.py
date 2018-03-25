from django.urls import path
from django.conf.urls import include, url

from . import views
app_name = 'ShoppingCart'

urlpatterns = [
    path('shoppingcart/', views.shopping_cart, name='shoppingcart'),
    url(r'^shoppingcart/(?P<ticket_id>\d+)/$', views.shopping_cart, name='shoppingcart'),
]
