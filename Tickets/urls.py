from django.urls import path, re_path
from django.conf.urls import include, url

from . import views
app_name = 'Tickets'

urlpatterns = [
    path('sports/', views.sports, name='sports'),
    path('concerts/', views.concerts, name='concerts'),
    path('arttheater/', views.arttheater, name='arttheater'),
    # path('test/', views.test, name='test'),
    path('sports/<int:ticket_id>/', views.view_sport_ticket, name='viewsportticket'),
    path('arttheater/<int:ticket_id>/', views.view_art_ticket, name='viewartticket'),
    path('concerts/<int:ticket_id>/', views.view_concert_ticket, name='viewconcertticket'),
    path('sports/<int:ticket_id>/<int:quantity>', views.add_to_cart, name='add_ticket'),
    path('arttheater/<int:ticket_id>/<int:quantity>', views.add_to_cart, name='add_ticket'),
    path('concerts/<int:ticket_id>/<int:quantity>', views.add_to_cart, name='add_ticket'),
    path('cart/', views.get_cart, name='cart'),
    path('<int:ticket_id>', views.remove_from_cart, name='remove'),
    path('', views.total_cart, name='total'),
    path('cart/<int:ticket_id>/<int:quantity>/<str:price>', views.update_item, name='update'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.add_to_table, name='success')
    # path('', auth_views.login, {'template_name': 'registration/login.html'}, name='login')
]
