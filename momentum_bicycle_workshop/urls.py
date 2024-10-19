from django.contrib import admin
from django.urls import path, include  # Ensure 'include' is imported

urlpatterns = [
    path('', include('myapp.urls')), 
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Include authentication URLs
]
