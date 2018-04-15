from .forms import CustomUserCreationForm, PickTicketDates
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.shortcuts import render, redirect
from Tickets.views import count_items
from Tickets.models import Ticket, Order, OrderDetail
import datetime
from django.contrib.auth.models import User

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
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            set_success(True)
            success = get_success()
            #print(success)
            return render(request, 'Home/account.html', {'success': success})
        else:
            messages.error(request, 'Please correct the error below.')
            set_success(False)
            success = get_success()
            #print(success)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'Home/account.html', {
        'form': form,
        'count': total
    })


def index(request):
    total = count_items(request)
    return render(request, 'Home/index.html', {'count': total})


def helps(request):
    total = count_items(request)
    return render(request, 'Home/help.html', {'count': total})


def happeningsoon(request):
    total = count_items(request)
    return render(request, 'Home/happeningsoon.html', {'count': total})


def deals(request):
    total = count_items(request)
    return render(request, 'Home/deals.html', {'count': total})


def showticketsbydate(request):
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

    return render(request, 'Home/ticketsbydate.html', {'ticketsbydate': ticketlist,\
                                                        'form': pickedDateForms,\
                                                       'startdate': startdate, 'enddate': enddate})


def showticketslowquant(request):
    ticketlist = []
    tickets = Ticket.objects.filter(qty__lt=60)

    for ticket in tickets:
        ticketlist.append(ticket)

    return render(request, 'Home/ticketslowquant.html', {'lowtickets': ticketlist})


def pastpurchases(request):
    user = request.user

    userid = str(user.id)

    if userid == 'None':
        message = "You must be logged in to view past purchases"
        return render(request, 'Home/account.html', {'message': message})

    else:
        message = "Past purchases for " + str(user)
        purchaselist = []
        orders = OrderDetail.objects.filter(id=userid).select_related()
        for order in orders:
            purchaselist.append(order)
        return render(request, 'Home/account.html', {'message': message, 'purchaselist': purchaselist})

