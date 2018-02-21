from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return render(request, 'Home/index.html')


def modal(request):
    return render(request, 'registration/login.html')
