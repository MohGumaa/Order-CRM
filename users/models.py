from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(null=True, blank=True)
    dated_created = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.user) if self.user else self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor')
    )

    name = models.CharField(max_length=200)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    dated_created = models.DateField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivery', 'Delivery')
    )

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    dated_created = models.DateField(auto_now_add=True, null=True)
    note = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.product.name
