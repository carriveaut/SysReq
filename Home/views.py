from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('index')
    template_name = 'Registration/signup.html'


def index(request):
    return render(request, 'Home/index.html')


def modal(request):
    return render(request, 'registration/login.html')
