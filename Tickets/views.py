from django.shortcuts import render


def sports(request):
    return render(request, 'Tickets/sports.html')


def concerts(request):
    return render(request, 'Tickets/concerts.html')


def arttheater(request):
    return render(request, 'Tickets/arttheater.html')
