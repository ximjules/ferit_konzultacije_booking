from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('booking.urls')),  # dodano: routing aplikacije booking na root
]

# Dodaj ovo na dnu radi serviranja static fajlova u developmentu
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT or (settings.BASE_DIR / "static"))
