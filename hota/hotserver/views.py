from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.models import User;
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
import json
from django.db.models import Q

# Create your views here.


#login user
class LoginUser(APIView):
    def post(self, request):
        data = request.data
        print(data)
        username = data.get('username')
        password = data.get('pw')
        currentUser = User.objects.filter(username=username)
        if not currentUser.exists():
            return Response(status=status.HTTP_204_NO_CONTENT, data={'message':'Wrong username or passwaord'})
        authPass = User.objects.get(username=username).check_password(password)
        if not authPass:
            return Response(status=status.HTTP_204_NO_CONTENT, data={'message':'Wrong username or passwaord'})
        return Response(status=status.HTTP_200_OK, data={'message': 'You have been logged in successfully'})
        
class EmployeeView(APIView):
    def get(self, request):
        data = UserSerializer(User.objects.all(), many=True).data
        return Response(status=status.HTTP_200_OK, data=data)

class TableView(APIView):
    def get(self, req):
        tables = Table.objects.all()
        tableList = TableSerializer(tables, many=True).data
        return Response(status=status.HTTP_200_OK, data=tableList)
    
    def post(self, request):
         table_name = request.POST.get("table_name")
         Table(table_name=table_name).save()
         tables = Table.objects.all()
         serialData = TableSerializer(tables, many=True).data
         return Response(status=status.HTTP_201_CREATED, data=serialData)
    
    def delete(self, request):
        table = request.POST.get("table")
        TableSerializer(table).update()
        tables = TableSerializer(Table.objects.all()).data
        return Response(status=status.HTTP_200_OK, data=tables)

    def patch(self, request):
        table = request.POST.get("table")
        print(table)
        return Response(status=status.HTTP_200_OK, data={})
    

class ProductView(APIView):
    def get(self, request):
        food = Food.objects.all()
        dat = FoodSerializer(food, many=True).data
        return Response(status=status.HTTP_200_OK, data=dat)
    
    def post(self, request):
         createdProduct = FoodSerializer(request.POST).create()
         return Response(status=status.HTTP_200_OK, data=createdProduct)
    
    def patch(self, request):
        table = request.POST.get("table")
        updatedProd = TableSerializer(table).update()
        return Response(status=status.HTTP_200_OK, data=updatedProd)
    

class OrderView(APIView):
    def get(self, req):
        orderItems = Order.objects.all()
        dat = OrderSerializer(orderItems, many=True).data
        return Response(status=status.HTTP_200_OK, data=dat)
    
    def post(self, req):
        order = json.loads(req.body)
        table = None
        if order.get('table')==None:
            table= Table.objects.all().first()
        else:
            table =Table.objects.get(id = order.get('table').get('id'))
        amount = 0
        for item in order.get('items'):
            food = Food.objects.get(id=item.get('id'))
            amount += item.get('quantity') * food.price
        currentOrder = Order(table=table, isPaid = order.get('pay_status'), amount = amount)
        currentOrder.save()
        for item in order.get('items'):
            product = Food.objects.get(id= item.get('id'))
            OrderItem(order = currentOrder,product=product, quantity = item.get('quantity')).save() 
        for item in order.get('items'):
            food = Food.objects.get(id=item.get('id'))
            remaining = food.stock - item.get('quantity')
            food.stock = remaining
            food.save()
        return Response(status=status.HTTP_201_CREATED)


    def put(self, req):
        order = json.loads(req.body)
        oldOrder = Order.objects.get(id=order.get('id'))
        oldOrder.isBooked = order.get('isBooked')
        oldOrder.isCanceled = order.get('isCanceled')
        oldOrder.isServed = order.get('isServed')
        oldOrder.isPaid = order.get('isPaid')
        oldOrder.save()
        newData = OrderSerializer(Order.objects.filter(Q(isPaid=False) | Q(isServed = False), isCanceled = False), many=True).data
        return Response(status=status.HTTP_200_OK, data=newData)


class SaleView(APIView):
    def get(self, req):
        sales = Sale.objects.all()
        dat = SaleSerializer(sales, many=True).data
        return Response(status=status.HTTP_200_OK, data=dat)
        
    def delete(self, req):
        sale = req.POST
        Sale(sale).delete()
        return Response(status=status.HTTP_200_OK)
    

class ItemsView(APIView):
     def get(self, req):
        orderItems = OrderItem.objects.all()
        dat = OrderItemsSerializer(orderItems, many=True).data
        return Response(status=status.HTTP_200_OK, data=dat)




