from django.shortcuts import render


def shoppingcart(request):
    return render(request, 'ShoppingCart/shoppingcart.html')
