from django.shortcuts import render
from django_tables2 import tables
from .tables import TicketTable
import requests
import ticketpy
import json

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


def test(request):

    tm_client = ticketpy.ApiClient('3dRZUZyfxeZ1U6EP8BajzFCol7ZAtSFb')
    name = ''
    pages = tm_client.events.find(
        classification_name='Rock',
        state_code='MN',
        start_date_time='2018-01-01T20:00:00Z',
        end_date_time='2019-01-01T20:00:00Z'
    )
    concert = []
    vID = ''
    venueName = []
    var3 = []
    for page in pages:
        for event in page:
            concert.append(event.name)
            # vID = event.id
            # pages2 = tm_client.venues.find(
            #     id=vID
            # )
            # for page2 in pages2:
            #     for v in page2:
            #         venueName.append(v.name)
    return render(request, 'Tickets/test.html', {'name': concert})
    # return render(request, 'Tickets/test.html', {'name': concert}, {'venue': venueName})
