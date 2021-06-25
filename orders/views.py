from django.db import connection
from django.http.response import HttpResponse
from rest_framework.views import APIView
from orders.serializers import OrderSerializer
from orders.models import Order, OrderItem
from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.response import Response
from users.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from admin.pagination import CustomPagination
import csv


# Create your views here.
class OrderGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset =  Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = CustomPagination


    def get(self, request, pk=None):
        if pk:
            return Response({
                'data': self.retrieve(request,pk).data
            })
             
        return self.list(request)
 


class ExportAPIViw(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = "attachment; filename=orders.csv"

        orders = Order.objects.all()
        writer = csv.writer(response)

        writer.writerow(['ID', 'NAME', 'EMAIL', 'PRODUCT TITLE', 'PRICE', 'QUANTITY'])

        for order in orders:
            writer.writerow([order.id, order.name, order.email, '', '', ''])
            orderItem = OrderItem.objects.all().filter(order_id=order.id)

            for item in orderItem:
                writer.writerow(['', '','', item.product_title, item.price, item.quantity])

        return response


class ChartAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, _):
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT DATE_FORMAT(o.created_at, '%Y-%m-%d') as date, sum(i.quantity + i.price) as sum
            FROM orders_order as o
            JOIN orders_orderitem as i ON o.id = i.order_id
            GROUP BY date
            """)

            row = cursor.fetchall()

        return Response({
            'date': result[0],
            'sum': result[1] 
        } for result in row)


