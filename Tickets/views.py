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
from decimal import *


def sports(request):
    total = count_items(request)

    concertlist = []
    tickets = Ticket.objects.filter(classification="Sports",
                                    start_Date__gte=datetime.date.today(),
                                    qty__gte=0)
    for ticket in tickets:
        concertlist.append(ticket)

    table = TicketTable(concertlist)

    return render(request, 'Tickets/sports.html', {'table': table, 'count': total})


def concerts(request):
    total = count_items(request)

    concertlist = []
    tickets = Ticket.objects.filter(classification="Music",
                                    start_Date__gte=datetime.date.today(),
                                    qty__gte=0)
    for ticket in tickets:
        concertlist.append(ticket)

    table = TicketTable(concertlist, order_by="start_Date")

    return render(request, 'Tickets/concerts.html', {'table': table, 'count': total})


def arttheater(request):
    total = count_items(request)
    concertlist = []
    tickets = Ticket.objects.filter(classification="Arts & Theatre",
                                    start_Date__gte=datetime.date.today(),
                                    qty__gte=0)
    for ticket in tickets:
        concertlist.append(ticket)

    table = TicketTable(concertlist, order_by="start_Date")

    return render(request, 'Tickets/arttheater.html', {'table': table, 'count': total})


def view_sport_ticket(request, ticket_id):
    total = count_items(request)
    tickets = Ticket.objects.filter(id=ticket_id)
    today = datetime.datetime.now().date()
    end_date= today + datetime.timedelta(days=3)
    selected = object
    for ticket in tickets:
        if today <= ticket.start_Date:
            ticket.price = ticket.price * Decimal(.5)
            selected = ticket
        # if datetime.datetime.now() <= ticket.start_Date:
        #     ticket.price = ticket.price * Decimal(.5)
        #     selected = ticket
        # else:
        #     ticket.price = ticket.price * Decimal(.5)
        #     selected = ticket
        else:
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
    return HttpResponseRedirect('/Tickets/cart/')


def update_item(request):
    ticket_id = request.POST.get("tick_id", 0)
    quantity = request.POST.get("qty", '')
    price = request.POST.get("price", 0.0)
    ticket = Ticket.objects.get(id=ticket_id)
    cart = Cart(request)
    cart.update(ticket, quantity, price)
    return get_cart(request)


def get_cart(request):
    suggested_type = ''                              # Hold suggested type.
    table = SuggestionTable({'Default': 'Default'})  # Initialize the SuggestionTable

    sport = 0           # Hold sports counts.
    art = 0             # Hold art counts.
    music = 0           # Hold music counts.

    cart = Cart(request)            # Get the cart.
    total = total_cart(request)     # Get the cart total.
    count = count_items(request)    # Get the total count for cart items.

    # Loop through the cart and accumulate the totals (by quantity)
    # for each classification of ticket in the cart.
    for item in cart:
        ticket = Ticket.objects.filter(id=item.object_id)
        for tick in ticket:
            if tick.classification == 'Sports':
                sport += item.quantity
            elif tick.classification == 'Arts & Theatre':
                art += item.quantity
            elif tick.classification == 'Music':
                music += item.quantity

    # Check to see if Sport classification has more tickets
    # in cart than Art and Music.
    if sport > art and sport > music:
        table = suggestion_analytics(request, 'Sports')
        suggested_type = 'sports'

    # Check to see if Art classification has more tickets
    # in cart than Sport and Music.
    if art > music and art > sport:
        table = suggestion_analytics(request, 'Arts & Theatre')
        suggested_type = 'arts & theater'

    # Check to see if Music classification has more tickets
    # in cart than Art and Sport.
    if music > art and music > sport:
        table = suggestion_analytics(request, 'Music')
        suggested_type = 'music'

    return render(request, 'Tickets/cart.html', {'total': total,
                                                 'cart': cart,
                                                 'count': count,
                                                 'table': table,
                                                 'suggestion': suggested_type})


def suggestion_analytics(request, classification):
    suggestion = []  # Hold suggestion data.

    # Find a ticket that is 60 days out from today and is
    # in the classification found most in the user's cart.
    sell = Ticket.objects.filter(classification=classification,
                                 start_Date__gte=(datetime.date.today()
                                                  + datetime.timedelta(days=60)),
                                 on_sale=0)[:1]

    # Grab the first ticket and append it to the list.
    for item in sell:
        suggestion.append(item)

    # Return the Table with the data.
    return SuggestionTable(suggestion)


def checkout(request):
    count = count_items(request)            # Count the items in the Cart.
    sub_total = float(total_cart(request))  # Get the total from the Cart.
    shipping = float(16.99)                 # Default shipping cost.
    tax = float(.065)                       # Default tax cost.

    # Calculate the overall total and format.
    total = '${:,.2f}'.format(((sub_total*tax) + sub_total + shipping))

    if request.method == 'POST':

        # Request the information from the payment form.
        pay = PaymentForm(request.POST)

        # If the form was valid, than send user to the
        # success page. Otherwise stay on current page.
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
        shipping = float(16.99)
        tax = float(.065)
        msg += "{:3} {: <60} {: >10} {: >10} {: >14}".format(" ", "Event", "Price", "Quantity", "Total Price")
        for item in Cart(request):
            # msg = '\n' + msg + " " + str(count) + ". " + item.product.event + " $" + str(item.product.price) + " "
            # + str(item.quantity) + "qty  $" + str(item.total_price) + "\n"
            # msg2 = msg + '{0:3}{1:<60}{2:>10}{3:>10}{4:>10}\n'
            # msg = msg2.format(str(count) + ".", item.product.event, "$" + str(item.product.price),
            #                   str(item.quantity) + "qty. ", "$" + str(item.total_price))
            msg += "\n{:3} {: <60} {: >10} {: >10} {: >14}".format(str(count),
                                                                   item.product.event,
                                                                   '${:,.2f}'.format(item.product.price),
                                                                   item.quantity,
                                                                   '${:,.2f}'.format(item.total_price))

            total = total + float(item.total_price)
            count = count + 1
        total = total + (total * tax)
        msg += '\n\n{:<82}{:>10}:{:>8} '.format(" ", "Tax", str(tax))
        msg += '\n{:<82}{:>10}:{:>8}'.format(" ", "Shipping", '${:,.2f}'.format(shipping))
        msg += '\n{:<82}{:>10}:{:>8}'.format(" ", "Total", '${:,.2f}'.format(total))
        msg += '\n\n' + request.POST.get("ShipName", "") + ', we at Ticket Portal appreciate your purchase! Thank you!'
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
    # Retrieve the cart.
    cart = Cart(request)

    # Retrieve the current user.
    user = request.user

    # Check if this purchase was an anonymous
    # user purchase and save order.
    if request.user.is_anonymous:
        order = Order(user=None)
        order.save()
    else:
        order = Order(user=user)
        order.save()

    # Retrieve the items out of the cart.
    item = Item.objects.filter(cart_id=cart.cart.pk)

    # Add the details of the item to the
    # OrderDetails model.
    for i in item:
        detail = OrderDetail(order=order,
                             ticket=Ticket(i.object_id),
                             quantity=i.quantity,
                             price=i.unit_price)

        # Get the Ticket quantity from the Ticket object
        # based on the ticket ID from the item.
        tick = Ticket.objects.filter(id=i.object_id).values_list('qty', flat=True)

        # Take the Ticket object quantity and subtract
        # the purchased quantity.
        change_qty = tick[0]-i.quantity

        # Update the Quantity that is left for the Ticket object.
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
