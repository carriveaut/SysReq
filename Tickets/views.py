from django.shortcuts import render, HttpResponseRedirect,  render_to_response
from .tables import TicketTable
import datetime
from Tickets.models import Ticket
import ticketpy
from cart.cart import Cart


def sports(request):
    total = count_items(request)

    concertlist = []
    tickets = Ticket.objects.filter(classification="Sports", start_Date__gte=datetime.date.today())
    for ticket in tickets:
        concertlist.append(ticket)

    table = TicketTable(concertlist)

    return render(request, 'Tickets/sports.html', {'table': table, 'count': total})


def concerts(request):
    total = count_items(request)

    concertlist = []
    tickets = Ticket.objects.filter(classification="Music", start_Date__gte=datetime.date.today())
    for ticket in tickets:
        concertlist.append(ticket)

    table = TicketTable(concertlist, order_by="start_Date")

    return render(request, 'Tickets/concerts.html', {'table': table, 'count': total})


def arttheater(request):
    total = count_items(request)
    concertlist = []
    tickets = Ticket.objects.filter(classification="Arts & Theatre", start_Date__gte=datetime.date.today())
    for ticket in tickets:
        concertlist.append(ticket)

    table = TicketTable(concertlist, order_by="start_Date")

    return render(request, 'Tickets/arttheater.html', {'table': table, 'count': total})


def view_sport_ticket(request, ticket_id):
    total = count_items(request)
    tickets = Ticket.objects.filter(id=ticket_id)
    selected = object
    for ticket in tickets:
        selected = ticket
    return render(request, 'Tickets/viewticket.html', {'selected': selected, 'count': total})


def view_art_ticket(request, ticket_id):
    total = count_items(request)
    tickets = Ticket.objects.filter(id=ticket_id)
    selected = object
    for ticket in tickets:
        selected = ticket
    return render(request, 'Tickets/viewticket.html', {'selected': selected, 'count': total})


def view_concert_ticket(request, ticket_id):
    total = count_items(request)
    tickets = Ticket.objects.filter(id=ticket_id)
    selected = object
    for ticket in tickets:
        selected = ticket
    return render(request, 'Tickets/viewticket.html', {'selected': selected, 'count': total})


# CART
def count_items(request):
    cart = Cart(request)
    cart.count()
    return cart.count()


def total_cart(request):
    cart = Cart(request)
    return cart.summary()


def add_to_cart(request, ticket_id, quantity):
    ticket = Ticket.objects.get(id=ticket_id)
    cart = Cart(request)
    cart.add(ticket, ticket.price, quantity)
    return get_cart(request)


def remove_from_cart(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    cart = Cart(request)
    cart.remove(ticket)
    return get_cart(request)


def update_item(request, ticket_id, quantity, price):
    ticket = Ticket.objects.get(id=ticket_id)
    cart = Cart(request)
    cart.update(ticket, quantity, price)
    return get_cart(request)


def get_cart(request):
    total = total_cart(request)
    count = count_items(request)
    return render(request, 'Tickets/cart.html', {'total': total,
                                                 'cart': Cart(request),
                                                 'count': count})


# AREA FOR CODE TESTS #
def test(request):
    # code for querying db
    # currently filters by sports
    # concertlist = []
    # tickets = Ticket.objects.filter(classification="Art")
    # for ticket in tickets:
    #     concertlist.append(ticket)

    # uncomment the following to add all sporting events for the year

    tm_client = ticketpy.ApiClient('3dRZUZyfxeZ1U6EP8BajzFCol7ZAtSFb')

    pages = tm_client.events.find(
        classification_name='Music',
        state_code='MN',
        start_date_time='2018-01-01T20:00:00Z',
        end_date_time='2019-01-01T20:00:00Z'
    )

    concertlist = []
    imageList = []

    for page in pages:
        for event in page:
            ticket = Ticket()
            print(event)
            print(event.__dict__.keys())
            print("Name: ", event.name)
            ticket.event = event.name

            for v in event.venues:
                ticket.venue_Name = v.name
                if v.images is not None:
                    for h in v.images:
                        # print(h)
                        if h['ratio'] == '16_9':
                            # imageList.append(h['url'])
                            ticket.image_Url = h['url']

                # ticket.venue_Name = v.name

            print("Venue More: ", event.venues[0])
            ticket.venue_Info = event.venues[0]

            print("Date: ", event.local_start_date)
            ticket.start_Date = event.local_start_date

            print("Time: ", event.local_start_time)
            # if event.local_start_time is None:
            #     ticket.start_Time = ('16')
            ticket.start_Time = event.local_start_time

            print("Status: ", event.status)
            ticket.status = event.status

            print("Classification: ", event.classifications[0].segment)
            ticket.classification = event.classifications[0].segment

            if not event.price_ranges:
                print("Event has no price range")
                # ticket.price = 99.99

            else:
                print("Min Price: ", event.price_ranges[0].get('min'))
                ticket.price = event.price_ranges[0].get('min')
                # print("Max Price: ", event.price_ranges[0].get('max'))
                # price_range = str(event.price_ranges[0].get('min')) + "-" + str(event.price_ranges[0].get('max'))
                # ticket.price_Range = price_range
            print("")
            ticket.save()
            concertlist.append(ticket)
    print(imageList)
    return render(request, 'Tickets/test.html', {'name': imageList})
    # return render(request, 'Tickets/test.html', {'name': concert}, {'venue': venueName})
