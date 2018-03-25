from django.urls import path
from django.conf.urls import include, url

from . import views
app_name = 'ShoppingCart'

urlpatterns = [
    path('shoppingcart/', views.get_cart, name='shoppingcart'),
    path('add/<int:ticket_id><int:quantity>', views.add_to_cart, name='add')
    # url(r'^shoppingcart/(?P<ticket_id>\d+)/$', views.shopping_cart, name='shoppingcart'),
]
