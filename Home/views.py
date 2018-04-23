from .forms import CustomUserCreationForm, PickTicketDates
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.shortcuts import render, redirect
from Tickets.views import *
from Tickets.models import Ticket, Order, OrderDetail
import datetime
from cart.cart import Cart
from django.contrib.auth.models import User
from decimal import *
from Tickets.tables import *

# class SignUpView(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('index')
#     template_name = 'Registration/signup.html'
success = False
badData = "False"


def set_success(suc):
    global success
    success = suc


def get_success():
    return success


def register(request):
    noGood = "False"
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            set_success(True)
            success = get_success()
            #print(success)
            return render(request, 'Home/index.html', {'success': success})
        else:
            noGood = "True"
            messages.error(request, "Error")
            set_success(False)
            success = get_success()

            #print(success)
    else:
        f = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': f, 'badData': noGood})


def change_password(request):
    total = count_items(request)
    transactions = build_transaction_history(request)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            set_success(True)
            success = get_success()
            #print(success)
            return render(request, 'Home/account.html', {'success': success,
                                                         'transactions': transactions,
                                                         'count': total})
        else:
            messages.error(request, 'Please correct the error below.')
            set_success(False)
            success = get_success()
            #print(success)
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'Home/account.html', {
        'form': form,
        'count': total,
        'transactions': transactions
    })


def build_transaction_history(request):
    transaction_list = []
    event_name = ''
    orders = Order.objects.filter(user=request.user)

    for order in orders:
        stuff = OrderDetail.objects.filter(order=order)
        date = order.complete_date.date()
        for this in stuff:
            item = Ticket.objects.filter(id=this.ticket_id)
            for name in item:
                event_name = name.event
            order_id = this.order_id
            quantity = this.quantity
            subtotal = (this.quantity * this.price)
            pre_list = {'order_id': order_id,
                        'event': event_name,
                        'quantity': quantity,
                        'subtotal': subtotal,
                        'date': date}
            transaction_list.append(pre_list)

    return transaction_list


def index(request):
    total = count_items(request)
    return render(request, 'Home/index.html', {'count': total})


def helps(request):
    total = count_items(request)
    return render(request, 'Home/help.html', {'count': total})


def view_ticket(request, ticket_id):
    total = count_items(request)
    tickets = Ticket.objects.filter(id=ticket_id)
    selected = object
    for ticket in tickets:
        selected = ticket
    return render(request, 'Tickets/viewticket.html', {'selected': selected, 'count': total})


def happeningsoon(request):
    total = count_items(request)
    ticketlist = []
    today = datetime.datetime.now()

    if request.method == 'POST':
        startDateStr = request.POST['start_date_year'] + " " + request.POST['start_date_month'] + " " \
                       + request.POST['start_date_day']

        endDateStr = request.POST['end_date_year'] + " " + request.POST['end_date_month'] + " " \
                     + request.POST['end_date_day']

        pickedDateForms = PickTicketDates(request.POST)
        pickedDateForms.start_date = datetime.datetime.strptime(startDateStr, '%Y %m %d')
        pickedDateForms.end_date = datetime.datetime.strptime(endDateStr, '%Y %m %d')

    else:
        pickedDateForms = PickTicketDates()
        pickedDateForms.start_date = today
        pickedDateForms.end_date = today + datetime.timedelta(days=7)

    tickets = Ticket.objects.filter(start_Date__gte=pickedDateForms.start_date,
                                    start_Date__lte=pickedDateForms.end_date)

    for ticket in tickets:
        ticketlist.append(ticket)

    table = HappeningSoonTable(ticketlist, order_by="start_Date")

    return render(request, 'Home/happeningsoon.html', {'ticketsbydate': ticketlist,
                                                       'table': table,
                                                       'count': total})
    # return render(request, 'Home/happeningsoon.html', {'count': total})


def add_to_cart(request, ticket_id, quantity):
    ticket = Ticket.objects.get(id=ticket_id)
    cart = Cart(request)
    cart.add(ticket, ticket.price, quantity)
    return HttpResponseRedirect('/Tickets/cart/')


def deals(request):
    total = count_items(request)
    ticketlist = []
    today = datetime.datetime.now()

    if request.method == 'POST':
        startDateStr = request.POST['start_date_year'] + " " + request.POST['start_date_month'] + " " \
                       + request.POST['start_date_day']

        endDateStr = request.POST['end_date_year'] + " " + request.POST['end_date_month'] + " " \
                     + request.POST['end_date_day']

        pickedDateForms = PickTicketDates(request.POST)
        pickedDateForms.start_date = datetime.datetime.strptime(startDateStr, '%Y %m %d')
        pickedDateForms.end_date = datetime.datetime.strptime(endDateStr, '%Y %m %d')

    else:
        pickedDateForms = PickTicketDates()
        pickedDateForms.start_date = today
        pickedDateForms.end_date = today + datetime.timedelta(days=3)

    tickets = Ticket.objects.filter(start_Date__gte=pickedDateForms.start_date,
                                    start_Date__lte=pickedDateForms.end_date,
                                    qty__gte=40)
    print(datetime.datetime.now() + datetime.timedelta(days=3))
    for ticket in tickets:
        ticket.price = ticket.price * Decimal(.5)
        ticketlist.append(ticket)

    startdate = datetime.datetime.date(pickedDateForms.start_date)
    enddate = datetime.datetime.date(pickedDateForms.end_date)
    return render(request, 'Home/deals.html', {'ticketsbydate': ticketlist,
                                                       'form': pickedDateForms,
                                                       'startdate': startdate,
                                                       'enddate': enddate,
                                                       'count': total})


def showticketsbydate(request):
    total = count_items(request)
    ticketlist = []
    today = datetime.datetime.now()

    if request.method == 'POST':
        startDateStr = request.POST['start_date_year'] + " " + request.POST['start_date_month'] + " "\
                       + request.POST['start_date_day']

        endDateStr = request.POST['end_date_year'] + " " + request.POST['end_date_month'] + " "\
                + request.POST['end_date_day']

        pickedDateForms = PickTicketDates(request.POST)
        pickedDateForms.start_date = datetime.datetime.strptime(startDateStr, '%Y %m %d')
        pickedDateForms.end_date = datetime.datetime.strptime(endDateStr, '%Y %m %d')

    else:
        pickedDateForms = PickTicketDates()
        pickedDateForms.start_date = today
        pickedDateForms.end_date = today + datetime.timedelta(days=14)

    tickets = Ticket.objects.filter(start_Date__gte=pickedDateForms.start_date,
                                    start_Date__lte=pickedDateForms.end_date)

    for ticket in tickets:
        ticketlist.append(ticket)

    startdate = datetime.datetime.date(pickedDateForms.start_date)
    enddate = datetime.datetime.date(pickedDateForms.end_date)

    return render(request, 'Home/ticketsbydate.html', {'ticketsbydate': ticketlist,
                                                       'form': pickedDateForms,
                                                       'startdate': startdate,
                                                       'enddate': enddate,
                                                       'count': total})


def showticketslowquant(request):
    total = count_items(request)
    ticketlist = []
    tickets = Ticket.objects.filter(qty__lt=10)

    for ticket in tickets:
        ticketlist.append(ticket)

    return render(request, 'Home/ticketslowquant.html', {'lowtickets': ticketlist,
                                                         'count': total})


def saveaccount(request):
    if request.method == 'POST':
        first_name = request.POST.get("FirstName")
        last_name = request.POST.get("LastName")
        email = request.POST.get("Email")
        # print(first_name, last_name, email)
        User.objects.filter(id=request.user.id).update(first_name=first_name, last_name=last_name, email=email)
        return render(request, 'Home/account.html')
# def pastpurchases(request):
#     user = request.user
#
#     userid = str(user.id)
#
#     if userid == 'None':
#         message = "You must be logged in to view past purchases"
#         return render(request, 'Home/account.html', {'message': message})
#
#     else:
#         message = "Past purchases for " + str(user)
#         purchaselist = []
#         orders = Order.objects.filter(user=userid)
#         for order in orders:
#             print(order)
#         return render(request, 'Home/account.html', {'message': message,
#                                                      'purchaselist': purchaselist})

