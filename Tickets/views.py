from django.shortcuts import render
from django_tables2 import tables
from .tables import TicketTable
import datetime
from Tickets.models import Ticket
import requests
import ticketpy
import json

from .models import Ticket

def sports(request):
    data = [{'event': 'MN Wild', 'location': 'Xcel Energy Center', 'time': '7:30 PM'},
            {'event': 'NCHC College Hockey Frozen', 'location': 'Xcel Energy Center', 'time': '4:00 PM'},
            {'event': 'U of M Baseball', 'location': 'U. S. Bank Stadium', 'time': '6:30 PM'}]

    table = TicketTable(data)

    return render(request, 'Tickets/sports.html', {'table': table})


def concerts(request):
    data = [{'event': 'Sum41', 'location': 'Varsity Theater', 'time': '8:00 PM'},
            {'event': 'Jake Owen', 'location': 'Treasure Island Resort & Casino', 'time': '8:00 PM'},
            {'event': 'P!NK: Beautiful Trauma World Tour', 'location': 'Xcel Energy Center', 'time': '7:30 PM'}]

    table = TicketTable(data)

    return render(request, 'Tickets/concerts.html', {'table': table})


def arttheater(request):
    data = [{'event': 'Minnesota\'s Ballet\'s Swan Lake', 'location': 'Orpheum Theatre', 'time': '7:00 PM'},
            {'event': 'The Illusionists - Live From Broadway (Touring)', 'location': 'Orpheum Theatre', 'time': '8:00 PM'},
            {'event': 'Puddles Pity Party', 'location': 'Pantages Theatre', 'time': '7:30 PM'}]

    table = TicketTable(data)

    return render(request, 'Tickets/arttheater.html', {'table': table})


def view_ticket(request):
    return render(request, 'Tickets/viewticket.html')


def test(request):
    # code for querying db
    # currently filters by sports
    concertlist = []
    tickets = Ticket.objects.filter(classification="Art")
    for ticket in tickets:
        concertlist.append(ticket)

    # uncomment the following to add all sporting events for the year

    tm_client = ticketpy.ApiClient('3dRZUZyfxeZ1U6EP8BajzFCol7ZAtSFb')

    pages = tm_client.events.find(
        classification_name='Art',
        state_code='MN',
        start_date_time='2018-01-01T20:00:00Z',
        end_date_time='2019-01-01T20:00:00Z'
    )

    # concertlist = []
    #
    # for page in pages:
    #     for event in page:
    #         ticket = Ticket()
    #         # print(event)
    #         # print(event.__dict__.keys())
    #         print("Name: ", event.name)
    #         ticket.event = event.name
    #
    #         print("Venues: ", event.venues[0])
    #         ticket.venues = event.venues[0]
    #
    #         print("Date: ", event.local_start_date)
    #         ticket.start_Date = event.local_start_date
    #
    #         print("Time: ", event.local_start_time)
    #         # if event.local_start_time is None:
    #         #     ticket.start_Time = ('16')
    #         ticket.start_Time = event.local_start_time
    #
    #         print("Status: ", event.status)
    #         ticket.status = event.status
    #
    #         print("Classification: ", event.classifications[0].segment)
    #         ticket.classification = event.classifications[0].segment
    #
    #         if not event.price_ranges:
    #             print("Event has no price range")
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
