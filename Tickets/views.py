from django.shortcuts import render
from django_tables2 import tables
from .tables import TicketTable
from Tickets.models import Ticket
import requests
import ticketpy
import json

from .models import Ticket

def sports(request):
    # data = [{'event': 'Wild', 'location': 'Saint Cloud State', 'time': '8:00'},
    #         {'event': 'Vikings', 'location': 'Target Field', 'time': '12:00'},
    #         {'event': 'Twins', 'location': 'Target Field', 'time': '1:30'}]

    concertlist = []
    tickets = Ticket.objects.filter(classification="Sports")
    for ticket in tickets:
        concertlist.append(ticket)

    table = TicketTable(concertlist)

    return render(request, 'Tickets/sports.html', {'table': table})

    # return render(request, 'Tickets/sports.html', {'table': table})


def concerts(request):
    return render(request, 'Tickets/concerts.html')


def arttheater(request):
    return render(request, 'Tickets/arttheater.html')


def test(request):
    # code for querying db
    # currently filters by sports
    concertlist = []
    tickets = Ticket.objects.filter(classification="Sports")
    for ticket in tickets:
        concertlist.append(ticket)

    # # uncomment the following to add all sporting events for the year
    #
    # tm_client = ticketpy.ApiClient('3dRZUZyfxeZ1U6EP8BajzFCol7ZAtSFb')
    #
    # pages = tm_client.events.find(
    #     classification_name='Sports',
    #     state_code='MN',
    #     start_date_time='2018-01-01T20:00:00Z',
    #     end_date_time='2019-01-01T20:00:00Z'
    # )

    # concertlist = []
    #
    # for page in pages:
    #     for event in page:
    #         ticket = Ticket()
    #         # print(event)
    #         # print(event.__dict__.keys())
    #         # print("Name: ", event.name)
    #         ticket.event = event.name
    #
    #         # print("Venues: ", event.venues[0])
    #         ticket.venues = event.venues[0]
    #
    #         # print("Date: ", event.local_start_date)
    #         ticket.start_Date = event.local_start_date
    #
    #         # print("Status: ", event.status)
    #         ticket.status = event.status
    #
    #         # print("Classification: ", event.classifications[0].segment)
    #         ticket.classification = event.classifications[0].segment
    #
    #         if not event.price_ranges:
    #             # print("Event has no price range")
    #             ticket.price_Range = "No Price Range"
    #
    #         else:
    #             print("Min Price: ", event.price_ranges[0].get('min'))
    #             print("Max Price: ", event.price_ranges[0].get('max'))
    #             price_range = str(event.price_ranges[0].get('min')) + "-" + str(event.price_ranges[0].get('max'))
    #             ticket.price_Range = price_range
    #         print("")
    #         ticket.save()
    #         concertlist.append(ticket)

    return render(request, 'Tickets/test.html', {'name': concertlist})
    # return render(request, 'Tickets/test.html', {'name': concert}, {'venue': venueName})
