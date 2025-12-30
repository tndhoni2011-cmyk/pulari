from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Product, Order

# 1. Home Page View
def index(request):
    # Database-la irundhu products eduthu Home page-ku anupurom
    items = Product.objects.all()
    return render(request, 'intex.html', {'items': items})

# 2. Product Page View
def product_page(request):
    # Database-la irundhu products eduthu Product page-ku anupurom
    items = Product.objects.all()
    return render(request, 'product_page.html', {'items': items})

# 3. Order Logic
def create_order(request):
    if request.method == 'POST':
        try:
            # Frontend-la irundhu vara JSON data-vai padikirom
            data = json.loads(request.body)
            
            # MUKKIYAM: Unga Model Field names-ku etha maari inga save panrom
            order = Order.objects.create(
                customer_name=data.get('name'),  # JS 'name' -> Model 'customer_name'
                phone=data.get('phone'),
                email=data.get('email'),
                product=data.get('product'),     # JS 'product' -> Model 'product'
                quantity=data.get('quantity'),
                message=data.get('message')
            )
            
            # Success response anupurom
            return JsonResponse({'status': 'success', 'order_id': order.id})
            
        except Exception as e:
            # Error vandha '400 Bad Request' anupurom
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
    return JsonResponse({'status': 'error', 'message': 'Only POST allowed'}, status=405)