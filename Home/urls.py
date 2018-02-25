from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib import admin

from . import views
app_name = 'Home'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.register, name='signup')
    # path('signup/', views.SignUpView.as_view(), name='signup')
    # path('', auth_views.login, {'template_name': 'registration/login.html'}, name='login')
]
