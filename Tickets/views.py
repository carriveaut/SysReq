from django.shortcuts import render
from django_tables2 import tables
from .tables import TicketTable


def sports(request):
    data = [{'event': 'Wild', 'location': 'Saint Cloud State', 'time': '8:00'},
            {'event': 'Vikings', 'location': 'Target Field', 'time': '12:00'},
            {'event': 'Twins', 'location': 'Target Field', 'time': '1:30'}]

    table = TicketTable(data)

    return render(request, 'Tickets/sports.html', {'table': table})


def concerts(request):
    return render(request, 'Tickets/concerts.html')


def arttheater(request):
    return render(request, 'Tickets/arttheater.html')
