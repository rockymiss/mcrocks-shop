import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from products.models import Products
from user_profiles.models import UserProfile

# Create your models here.


class Discount(models.Model):
    """
    A Model to allow the user to enter a discount code
    """
    discount_code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, null=False, default=0)

    def __str__(self):
        return self.discount_code


class Order(models.Model):
    """
    Class so that the user can order items and input their information
    for delivery  *Followed the boutique ado walkthrough for this model class
    with minor changes
    """
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='orders')
    full_name = models.CharField(max_length=55, null=False, blank=False)
    email = models.EmailField(max_length=255, null=False, blank=False)
    phone_number = models.CharField(max_length=22, null=False, blank=False)
    country = CountryField(max_length=40, blank_label='Country *',
                           null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    address1 = models.CharField(max_length=80, null=False, blank=False)
    address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    original_cart = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False,
                                  blank=False, default="")
    discount_code = models.ForeignKey(Discount, on_delete=models.SET_NULL,
                                      null=True, blank=True, default=None)

    def _generate_order_number(self):
        """
        A method to generate a random unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        A method to update grand total each time a line item is added,
        which accounts for delivery costs.
        """
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total')
            )['lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = (
                self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        else:
            self.delivery_cost = 0

        # Apply discount if applicable
        if self.discount_code:
            discount_percent = self.discount_code.discount_percentage
            discount_amount = (self.order_total * discount_percent / 100)
            self.discount_amount = discount_amount
            self.order_total -= discount_amount
            print(f"Discount applied: {self.discount_amount}")
        else:
            self.discount_amount = 0

        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        A method which overrides the original save method to set the order
        number if it hasn't been set previously.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """
    Class so that users can add products to their order which will
    also update delivery costs etc. as each items is added
    """
    order = models.ForeignKey(
        Order, null=False, blank=False, on_delete=models.CASCADE,
        related_name='lineitems')
    product = models.ForeignKey(
        Products, null=False, blank=False, on_delete=models.CASCADE)
    product_colour = models.CharField(max_length=20, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False,
        editable=False)

    def save(self, *args, **kwargs):
        """
        A method to override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product.product_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.name} on order {self.order.order_number}'
