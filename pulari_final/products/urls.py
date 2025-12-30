from django.urls import path
from . import views

urlpatterns = [
    # Home Page (intex.html)
    path('', views.index, name='home'),

    # Product Page
    path('product_page/', views.product_page, name='product_page'),

    # Order processing URL
    path('orders/create/', views.create_order, name='create_order'),
]