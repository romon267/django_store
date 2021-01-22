from django.forms import ModelForm
from store.models import ShippingAddress, Customer

class ShippingForm(ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'zipcode', 'state']


class GuestForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email']