from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('seeds', 'Seeds'),
        ('machines', 'Machinery'),
        ('fertilizer', 'Fertilizer'),
    ]
    #category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    #rating = models.FloatField()
    prodCount=models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Customer(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50,unique=True)
    password=models.CharField(max_length=50)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        if self.pk is None and self.password:
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'<Customer email : {self.email}, name: {self.name}>'

class Cart(models.Model):
    prodId = models.ForeignKey(Product,on_delete=models.CASCADE)
    prodCount=models.IntegerField(default=1)
    userId =models.ForeignKey(Customer,on_delete=models.CASCADE)

    def __str__(self):
        return f'< prodName : {self.prodId.name}, userId: {self.userId.id} > '