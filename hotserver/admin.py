from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([Profile, Food, Order, OrderItem, Table, Sale, ])
