from django.urls import path

from . import views
app_name = 'Tickets'

urlpatterns = [
    path('sports/', views.sports, name='sports'),
    path('concerts/', views.concerts, name='concerts'),
    path('arttheater/', views.arttheater, name='arttheater'),
    path('view-ticket/', views.view_ticket, name='viewticket'),
    # path('signup/', views.SignUpView.as_view(), name='signup')
    # path('', auth_views.login, {'template_name': 'registration/login.html'}, name='login')
]
