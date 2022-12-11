from django.shortcuts import render, redirect, reverse, get_object_or_404
from products.models import Products

# Create your views here.


def view_cart(request):
    """
    Returns the shopping cart view
    """
    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """
    Adds a quantity of the item the user selects to the Cart
    Also allows the user to tore the contents of the Cart when 
    browsing the website elsewhere
    """

    product = get_object_or_404(Products, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if item_id in list(cart.keys()):
        cart[item_id] += quantity
    else:
        cart[item_id] = quantity

    request.session['cart'] = cart
    return redirect(redirect_url)


def adjust_cart(request, item_id):
    """
    Adjusts the quantity from the cart template
    """

    quantity = int(request.POST.get('quantity', 0))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[item_id] = quantity
        print(quantity)
    else:
        cart.pop(item_id)
        print(quantity)

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))