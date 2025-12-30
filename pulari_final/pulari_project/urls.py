from django.contrib import admin
from django.urls import path, include
from django.conf import settings              # Idhu Mukkiyam
from django.conf.urls.static import static    # Idhu Romba Mukkiyam

urlpatterns = [
    path('admin/', admin.site.urls),
    # Products app URL link
    path('', include('products.urls')), 
]

# Indha code irundhal mattum dhaan Images work aagum!
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)