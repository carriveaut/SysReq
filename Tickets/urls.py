from django.urls import path

from . import views
app_name = 'Tickets'

urlpatterns = [
    path('sports/', views.sports, name='sports'),
    path('concerts/', views.concerts, name='concerts'),
    path('arttheater/', views.arttheater, name='arttheater'),
    path('test/', views.test, name='test'),
    path('sports/<int:ticket_id>/', views.view_sport_ticket, name='viewsportticket'),
    path('arttheater/<int:ticket_id>/', views.view_art_ticket, name='viewartticket'),
    path('concerts/<int:ticket_id>/', views.view_concert_ticket, name='viewconcertticket'),
    # path('signup/', views.SignUpView.as_view(), name='signup')
    # path('', auth_views.login, {'template_name': 'registration/login.html'}, name='login')
]
