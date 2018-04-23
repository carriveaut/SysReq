from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib import admin

from . import views
app_name = 'Home'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.register, name='signup'),
    path('account/', views.change_password, name='account'),
    path('faqs/', views.helps, name='faqs'),
    path('happeningsoon/', views.happeningsoon, name="happeningsoon"),
    path('deals/', views.deals, name="deals"),
    path('ticketsbydate/', views.showticketsbydate, name="ticketsbydate"),
    path('ticketslowquant/', views.showticketslowquant, name="ticketslowquant"),
    path('account', views.saveaccount, name="saveaccount"),
    path('happeningsoon/<int:ticket_id>/', views.view_ticket, name="view-ticket"),
    path('happeningsoon/<int:ticket_id>/<int:quantity>', views.add_to_cart, name='add_ticket'),
    path('deals/<int:ticket_id>/<int:quantity>', views.add_to_cart, name='add_ticket'),
    # path('pastpurchases/', views.pastpurchases, name="pastpurchases")
    # path('login/', views.login, name="login")
    # path('signup/', views.SignUpView.as_view(), name='signup')
    # path('', auth_views.login, {'template_name': 'registration/login.html'}, name='login')
]
