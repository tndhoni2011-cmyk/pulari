from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
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

# ============= ADMIN DASHBOARD VIEWS =============

# 4. Admin Dashboard - Product List with Stock
@login_required(login_url='admin:login')
def admin_dashboard(request):
    """Admin page with product list and stock information"""
    products = Product.objects.all()
    context = {
        'products': products,
        'total_products': products.count(),
        'low_stock_products': products.filter(stock__lt=10),  # Stock 10-ku bottom irundha low stock
    }
    return render(request, 'admin_dashboard.html', context)

# 5. Add Product
@login_required(login_url='admin:login')
@require_http_methods(["GET", "POST"])
def add_product(request):
    """Add new product"""
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            category = request.POST.get('category')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            description = request.POST.get('description')
            image = request.FILES.get('image') if request.FILES else None
            
            # Validation - Empty field check
            if not all([name, category, price, stock, description]):
                return render(request, 'add_product.html', {
                    'error': 'All fields are required!'
                })
            
            # Create product
            product = Product.objects.create(
                name=name,
                category=category,
                price=float(price),
                stock=int(stock),
                description=description,
                image=image if image else None
            )
            
            return redirect('admin_dashboard')
            
        except ValueError:
            return render(request, 'add_product.html', {
                'error': 'Price must be number, Stock must be integer!'
            })
        except Exception as e:
            return render(request, 'add_product.html', {
                'error': f'Error: {str(e)}'
            })
    
    return render(request, 'add_product.html')

# 6. Edit Product
@login_required(login_url='admin:login')
@require_http_methods(["GET", "POST"])
def edit_product(request, product_id):
    """Edit existing product"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        try:
            product.name = request.POST.get('name', product.name)
            product.category = request.POST.get('category', product.category)
            product.price = float(request.POST.get('price', product.price))
            product.stock = int(request.POST.get('stock', product.stock))
            product.description = request.POST.get('description', product.description)
            
            if request.FILES.get('image'):
                product.image = request.FILES['image']
            
            product.save()
            return redirect('admin_dashboard')
            
        except ValueError:
            return render(request, 'edit_product.html', {
                'product': product,
                'error': 'Price must be number, Stock must be integer!'
            })
    
    return render(request, 'edit_product.html', {'product': product})

# 7. Delete Product
@login_required(login_url='admin:login')
@require_http_methods(["POST"])
def delete_product(request, product_id):
    """Delete product with logic"""
    product = get_object_or_404(Product, id=product_id)
    
    try:
        # Logic: Check if product has pending orders
        pending_orders = Order.objects.filter(
            product=product.name,
            status__in=['new', 'processing']
        )
        
        if pending_orders.exists():
            return JsonResponse({
                'status': 'error',
                'message': f'Cannot delete! {pending_orders.count()} pending orders exist for this product.'
            }, status=400)
        
        product.delete()
        return JsonResponse({'status': 'success', 'message': 'Product deleted successfully!'})
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)