from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    dated_created = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.name} Customer'

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'{self.name} Tag'


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
        return f'({self.name})'

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivery', 'Delivery')
    )

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=200, choices=STATUS)
    dated_created = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f'Order staus: ({self.status})'
