from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('food/', ProductView.as_view(), name='products'),
    path('login/', LoginUser.as_view(), name='login'),
    path('orders/', OrderView.as_view(), name='orders'),
    path('tables/', TableView.as_view(), name='tables'),
    path('sales/', SaleView.as_view(), name='sales'),
    path('items/', ItemsView.as_view(), name='items'),
    path('employees/', EmployeeView.as_view(), name='items'),
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
