from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('books/', include('books.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('reviews/', include('reviews.urls')),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.views.custom_404'
handler403 = 'core.views.custom_403'
handler500 = 'core.views.custom_500'
