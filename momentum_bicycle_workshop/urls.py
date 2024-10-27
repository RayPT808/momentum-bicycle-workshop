from django.urls import path, include
from django.contrib import admin 
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import OwnerDashboardView 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('', include('myapp.urls')),
    path('owner/dashboard/', OwnerDashboardView.as_view(), name='owner_dashboard'),

    # Add other paths as needed
]

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
