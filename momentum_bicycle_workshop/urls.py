from django.contrib import admin
from django.urls import path, include  # Ensure 'include' is imported
from . import views

urlpatterns = [
    path('', include('myapp.urls')), 
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),    # Include authentication URLs
]
