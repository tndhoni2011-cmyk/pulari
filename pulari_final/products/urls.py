from django.urls import path
from . import views

urlpatterns = [
    # Home Page (intex.html)
    path('', views.index, name='home'),

    # Product Page
    path('product_page/', views.product_page, name='product_page'),

    # Order processing URL
    path('orders/create/', views.create_order, name='create_order'),
    
    # ===== ADMIN DASHBOARD URLS =====
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/product/add/', views.add_product, name='add_product'),
    path('admin/product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('admin/product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
]