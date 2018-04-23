from django.shortcuts import render, HttpResponseRedirect,  render_to_response
from .tables import *
from django.core import mail
from datetime import date, datetime
from django.core.mail import send_mail
from django.conf import settings
import datetime
from .models import Ticket, Checkout, Order, OrderDetail
import ticketpy
from cart.cart import Cart
from cart.models import Item
from .forms import CheckoutForm, PaymentForm
from django.contrib.auth.models import User


def sports(request):
    total = count_items(request)

    concertlist = []
    tickets = Ticket.objects.filter(classification="Sports", start_Date__gte=datetime.date.today(), qty__gte=0)
    for ticket in tickets:
        concertlist.append(ticket)

    table = TicketTable(concertlist)

    return render(request, 'Tickets/sports.html', {'table': table, 'count': total})


def concerts(request):
    total = count_items(request)

    concertlist = []
    tickets = Ticket.objects.filter(classification="Music", start_Date__gte=datetime.date.today(), qty__gte=0)
    for ticket in tickets:
        concertlist.append(ticket)

    table = TicketTable(concertlist, order_by="start_Date")

    return render(request, 'Tickets/concerts.html', {'table': table, 'count': total})


def arttheater(request):
    total = count_items(request)
    concertlist = []
    tickets = Ticket.objects.filter(classification="Arts & Theatre", start_Date__gte=datetime.date.today(), qty__gte=0)
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
    return HttpResponseRedirect('/Tickets/cart/')


def remove_from_cart(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    cart = Cart(request)
    cart.remove(ticket)
    return get_cart(request)


def update_item(request):
    ticket_id = request.POST.get("tick_id", 0)
    quantity = request.POST.get("qty", '')
    price = request.POST.get("price", 0.0)
    ticket = Ticket.objects.get(id=ticket_id)
    cart = Cart(request)
    cart.update(ticket, quantity, price)
    return get_cart(request)


def get_cart(request):
    suggestion = []
    suggested_type = ''
    table = SuggestionTable({'event': 'Hi'})
    sport = 0
    art = 0
    music = 0
    total = total_cart(request)
    count = count_items(request)
    cart = Cart(request)

    for item in cart:
        ticket = Ticket.objects.filter(id=item.object_id)
        for tick in ticket:
            if tick.classification == 'Sports':
                sport += item.quantity
            elif tick.classification == 'Arts & Theatre':
                art += item.quantity
            elif tick.classification == 'Music':
                music += item.quantity

    if sport > art and sport > music:
        sell = Ticket.objects.filter(classification='Sports',
                                     start_Date__gte=datetime.date.today())[:1]
        # print(sport)
        for item in sell:
            suggestion.append(item)
        table = SuggestionTable(suggestion)
        suggested_type = 'sports'

    if art > music and art > sport:
        sell = Ticket.objects.filter(classification='Arts & Theatre',
                                     start_Date__gte=datetime.date.today())[:1]
        # print(art)
        for item in sell:
            suggestion.append(item)
        table = SuggestionTable(suggestion)
        suggested_type = 'arts & theater'

    if music > art and music > sport:
        sell = Ticket.objects.filter(classification='Music',
                                     start_Date__gte=datetime.date.today())[:1]
        # print(music)
        for item in sell:
            suggestion.append(item)
        table = SuggestionTable(suggestion)
        suggested_type = 'music'

    return render(request, 'Tickets/cart.html', {'total': total,
                                                 'cart': cart,
                                                 'count': count,
                                                 'table': table,
                                                 'suggestion': suggested_type})


def checkout(request):
    c = Checkout()
    count = count_items(request)
    sub_total = float(total_cart(request))
    shipping = float(16.99)
    tax = float(.065)

    initial = (sub_total*tax) + sub_total + shipping
    total = ('%.2f' % initial).rstrip('0').rstrip('.')
    if request.method == 'POST':
        pay = PaymentForm(request.POST)
        if pay.is_valid():
            return HttpResponseRedirect('/Tickets/success/')
    else:
        pay = PaymentForm()

    return render(request, 'Tickets/checkout.html', {'cart': Cart(request),
                                                     'pay': pay,
                                                     'total': total,
                                                     'count': count,
                                                     'tax': tax,
                                                     'shipping': shipping})


def add_to_table(request):
    # start send_mail()
    if request.user.is_anonymous:
        username = None
    else:
        username = str(request.user.email)
        msg = 'Your receipt for your purchase ' + str(date.today().strftime('%b. %d %Y')) + ":\n\n"
        count = 1
        total = float(0.0)
        tax = float(.065)
        for item in Cart(request):
            # msg = '\n' + msg + " " + str(count) + ". " + item.product.event + " $" + str(item.product.price) + " " + str(item.quantity) + "qty  $" + str(item.total_price) + "\n"
            msg2 = msg + '{0:3}{1:<60}{2:>10}{3:>10}{4:>10}\n'
            msg = msg2.format(str(count) + ".", item.product.event, "$" + str(item.product.price),
                              str(item.quantity) + "qty. ", "$" + str(item.total_price))
            total = total + float(item.total_price)
            count = count + 1
        total = total + (total * tax)
        msg = msg + '     Tax: ' + str(tax) + '\n' + '     Total: ' + str(total)
        send_mail('Your receipt for your purchase ' + str(date.today().strftime('%b. %d %Y')), msg,
                  'theticketportal@gmail.com', [username], fail_silently=True, )
    # end send_mail()
    count = count_items(request)
    cart = Cart(request)
    add_to_order(request)
    cart.clear()
    c = Checkout()
    c.holder = request.POST.get("holder", "")
    c.number = request.POST.get("number", "")
    c.ccv_number = request.POST.get("ccv_number", "")
    month = request.POST.get("expiration_0", "")
    year = request.POST.get("expiration_1", "")
    expiration = month + '/' + year
    c.expiration = expiration
    c.ShipName = request.POST.get("ShipName", "")
    c.ShipAddress = request.POST.get("ShipAddress", "")
    c.ShipCity = request.POST.get("ShipCity", "")
    c.ShipState = request.POST.get("ShipState", "")
    c.ShipZip = request.POST.get("ShipZip", "")
    c.save()
    return render(request, 'Tickets/success_summary.html', {'count': count})


def add_to_order(request):
    cart = Cart(request)
    user = request.user
    if request.user.is_anonymous:
        order = Order(user=None)
        order.save()
    else:
        order = Order(user=user)
        order.save()

    item = Item.objects.filter(cart_id=cart.cart.pk)

    for i in item:
        detail = OrderDetail(order=order, ticket=Ticket(i.object_id), quantity=i.quantity, price=i.unit_price)

        tick = Ticket.objects.filter(id=i.object_id).values_list('qty', flat=True)
        # print(tick)
        change_qty = tick[0]-i.quantity
        Ticket.objects.filter(id=i.object_id).update(qty=change_qty)
        detail.save()


def myformat(x):
    return ('%.2f' % x).rstrip('0').rstrip('.')




# # AREA FOR CODE TESTS #
# def test(request):
#     # code for querying db
#     # currently filters by sports
#     # concertlist = []
#     # tickets = Ticket.objects.filter(classification="Art")
#     # for ticket in tickets:
#     #     concertlist.append(ticket)
#
#     # uncomment the following to add all sporting events for the year
#
#     tm_client = ticketpy.ApiClient('3dRZUZyfxeZ1U6EP8BajzFCol7ZAtSFb')
#
#     pages = tm_client.events.find(
#         classification_name='Music',
#         state_code='MN',
#         start_date_time='2018-01-01T20:00:00Z',
#         end_date_time='2019-01-01T20:00:00Z'
#     )
#
#     concertlist = []
#     imageList = []
#
#     for page in pages:
#         for event in page:
#             ticket = Ticket()
#             print(event)
#             print(event.__dict__.keys())
#             print("Name: ", event.name)
#             ticket.event = event.name
#
#             for v in event.venues:
#                 ticket.venue_Name = v.name
#                 if v.images is not None:
#                     for h in v.images:
#                         # print(h)
#                         if h['ratio'] == '16_9':
#                             # imageList.append(h['url'])
#                             ticket.image_Url = h['url']
#
#                 # ticket.venue_Name = v.name
#
#             print("Venue More: ", event.venues[0])
#             ticket.venue_Info = event.venues[0]
#
#             print("Date: ", event.local_start_date)
#             ticket.start_Date = event.local_start_date
#
#             print("Time: ", event.local_start_time)
#             # if event.local_start_time is None:
#             #     ticket.start_Time = ('16')
#             ticket.start_Time = event.local_start_time
#
#             print("Status: ", event.status)
#             ticket.status = event.status
#
#             print("Classification: ", event.classifications[0].segment)
#             ticket.classification = event.classifications[0].segment
#
#             if not event.price_ranges:
#                 print("Event has no price range")
#                 # ticket.price = 99.99
#
#             else:
#                 print("Min Price: ", event.price_ranges[0].get('min'))
#                 ticket.price = event.price_ranges[0].get('min')
#                 # print("Max Price: ", event.price_ranges[0].get('max'))
#                 # price_range = str(event.price_ranges[0].get('min')) + "-" + str(event.price_ranges[0].get('max'))
#                 # ticket.price_Range = price_range
#             print("")
#             ticket.save()
#             concertlist.append(ticket)
#     print(imageList)
#     return render(request, 'Tickets/test.html', {'name': imageList})
#     # return render(request, 'Tickets/test.html', {'name': concert}, {'venue': venueName})
