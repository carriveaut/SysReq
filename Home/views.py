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
    noGood = "False"
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            # messages.success(request, 'Account created successfully')
            return render(request, 'Home/index.html')
        else:
            noGood = "True"
            messages.error(request, "Error")
    else:
        f = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': f, 'badData': noGood})


def index(request):
    return render(request, 'Home/index.html')


def helps(request):
    return render(request, 'Home/help.html')


def happeningsoon(request):
    return render(request, 'Home/happeningsoon.html')


def deals(request):
    return render(request, 'Home/deals.html')


def account(request):
    return render(request, 'Home/account.html')

