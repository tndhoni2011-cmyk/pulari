from django.contrib import admin
from .models import Product, Order

# 1. Product Table-ai azhaga kaatta (Puthusa serthu iruken)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Admin list-la Name, Category, Price, Stock ellam theriyum
    list_display = ('name', 'category', 'price', 'stock') 
    list_filter = ('category',)
    search_fields = ('name', 'description')

# 2. Order Table (Unga code + Chinna improvement)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'phone', 'product', 'quantity', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'phone', 'product')
    
    # INDHA LINE MUKKIYAM:
    # Order-kulla pogamale, list page-laye 'Status' maathikalam!
    list_editable = ('status',)