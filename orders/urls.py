from django.urls import path
from .views import ChartAPIView, ExportAPIViw, OrderGenericAPIView

urlpatterns = [
    path('orders', OrderGenericAPIView.as_view()),
    path('orders/<str:pk>', OrderGenericAPIView.as_view()),
    path('export', ExportAPIViw.as_view()),
    path('chart', ChartAPIView.as_view()),

]
