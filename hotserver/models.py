from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_save
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True)

    def __str__(self):
        return self.user.first_name
    

class Food(models.Model):
    food_name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to='food_images', blank=True, null=True)
    isFrozen = models.BooleanField(default=False)
    stock = models.IntegerField(default=0)

    class Meta:
        ordering = ['food_name']

    def __str__(self):
        return self.food_name

class Table(models.Model):
    table_name = models.CharField(max_length=50, unique=True)
    isBooked = models.BooleanField(default=False)
    isFrozen = models.BooleanField(default=False)


    def __str__(self):
        return self.table_name

class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.PROTECT)
    amount = models.IntegerField(default = 0)
    isServed = models.BooleanField(default=False)
    isPaid = models.BooleanField(default=False)
    isBooked = models.BooleanField(default=False)
    isCanceled = models.BooleanField(default=False)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.table.table_name} {self.amount} {self.date} {self.time}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Food, on_delete=models.PROTECT)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.order.ref_number}  {self.product.food_name}'
    
class Sale(models.Model):
    ref_number = models.CharField(max_length=10)
    table_number = models.ForeignKey(Table, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.IntegerField()
    
    def __str__(self):
        return self.ref_number
    


