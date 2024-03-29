from django import forms
from .models import Order, Discount
from crispy_forms.helper import FormHelper


class OrderForm(forms.ModelForm):
    """
    Class for the form that is loaded when a user checks out
    """
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'address1', 'address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'address1': 'Address 1',
            'address2': 'Address 2',
            'county': 'County, State or Locality',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False


class DiscountForm(forms.ModelForm):
    """
    A form to allow the user to enter a discount code
    """

    class Meta:
        model = Discount
        fields = ['discount_code']


class AdminDiscount(forms.ModelForm):
    """
    A form to allow admin to create a new discount code and percentage
    """
    class Meta:
        model = Discount
        fields = ('discount_code', 'discount_percentage',)
