from django.shortcuts import render
from Tickets.models import Ticket
from .models import Cart

def shopping_cart(request, ticket_id):
    tickets = Ticket.objects.filter(id=ticket_id)
    selected = object
    for ticket in tickets:
    #     t = Ticket()
    #     c = Cart()
    #     c.ticketID = ticket.id
    #     c.cartPrice = ticket.price
    #     c.cartDate = '2019-02-10'
    #     c.cartQty = 3
        selected = ticket
    # request.session['theCart'] = c
    return render(request, 'ShoppingCart/shoppingcart.html', {'selected' : selected})
