from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls'), name='dashboard'),
    path('api/', include('api.urls'), name='api'),
    path('cart/', include('cart.urls'), name='cart'),
    path('shop/', include('shop.urls'), name='shop'),
    path('news/', include('news.urls'), name='news'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
