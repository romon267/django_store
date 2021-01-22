from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import OneToOneField

class Customer(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'Customer {self.id}, {self.name}, {self.email}'


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null = True, blank=True)

    def __str__(self):
        return f'Product {self.id}, {self.name}, {self.price}, {self.digital}'

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    status = models.CharField(max_length=20, default='', null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True)


    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for item in orderitems:
            if item.product.digital == False:
                shipping = True
        return shipping


    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems]) # generator for calculating cart total value
        return total

    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


    def __str__(self):
        return f'{self.id}, {self.customer.name} {self.customer.id}, {self.date_ordered}, trans_id: {self.transaction_id}'


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return f'{self.id}, {self.product.name} {self.product.id}, {self.order.id}'


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True, blank = True)
    city = models.CharField(max_length=200, null=True, blank = True)
    zipcode = models.CharField(max_length=200, null=True, blank = True)
    state = models.CharField(max_length=200, null=True, blank = True)
    date_added = models.DateTimeField(auto_now_add=True, blank = True)

    def __str__(self):
        return f'{self.id}, Customer: {self.order}'