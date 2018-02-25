from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.http import HttpResponse


# class SignUpView(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('index')
#     template_name = 'Registration/signup.html'


def register(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            # messages.success(request, 'Account created successfully')
            return render(request, 'Home/index.html')
    else:
        f = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': f})


def index(request):
    return render(request, 'Home/index.html')


def modal(request):
    return render(request, 'registration/login.html')

