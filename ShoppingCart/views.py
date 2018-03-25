# from django.shortcuts import render
# from Tickets.models import Ticket
# from .models import Cart
#
# def shopping_cart(request, ticket_id):
#     tickets = Ticket.objects.filter(id=ticket_id)
#     selected = object
#     for ticket in tickets:
#     #     t = Ticket()
#     #     c = Cart()
#     #     c.ticketID = ticket.id
#     #     c.cartPrice = ticket.price
#     #     c.cartDate = '2019-02-10'
#     #     c.cartQty = 3
#         selected = ticket
#     # request.session['theCart'] = c
#     return render(request, 'ShoppingCart/shoppingcart.html', {'selected' : selected})

from cart.cart import Cart
from Tickets.models import Ticket
from django.shortcuts import render_to_response


def add_to_cart(request, ticket_id, quantity):
    product = Ticket.objects.get(id=ticket_id)
    cart = Cart(request)
    cart.add(product, product.unit_price, quantity)


def remove_from_cart(request, ticket_id):
    product = Ticket.objects.get(id=ticket_id)
    cart = Cart(request)
    cart.remove(product)


def get_cart(request):
    return render_to_response('ShoppingCart/shoppingcart.html', dict(cart=Cart(request)))
