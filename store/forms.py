from django.forms import ModelForm
from store.models import ShippingAddress

class ShippingForm(ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'zipcode', 'state']