from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from cart.contexts import cart_contents

import stripe

# Create your views here.


def checkout(request):
    """
    Function to display the checkout form
    """

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = request.session.get('cart', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'address1': request.POST['address1'],
            'address2': request.POST['address2'],
            'county': request.POST['county'],
        }

    order_form = OrderForm(form_data)
    if order_form.is_valid():
        # order = order_form.save(commit=False)
        # pid = request.POST.get('client_secret').split('_secret')[0]
        # order.stripe_pid = pid
        # order.original_cart = json.dumps(cart)
        order_form.save()
        
        for item_id, item_data in cart.items():
            try:
                product = Products.objects.get(id=item_id)
                if isinstance(item_data, int):
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=item_data,
                    )
                    order_line_item.save()
                else:
                    for colour, quantity in item_data['items_by_colour'].items():
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=quantity,
                            product_colour=colour,
                        )
                        order_line_item.save()

            except Product.DoesNotExist:
                messages.error(request, (
                    "One of the items in your cart wasn't found in \
                    our database. Please call us for assistance!")
                )
                order.delete()
                return redirect(reverse('view_cart'))

    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing to see here!")
        return redirect(reverse('products'))

    current_cart = cart_contents(request)
    total = current_cart['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

    order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'stripe_public_key',
        'client_secret': 'intent.client_secret',
    }

    return render(request, template, context)
