from django.urls import path, include
from django.contrib import admin
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('', include('myapp.urls')),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('owner/dashboard/', views.OwnerDashboardView.as_view(), name='owner_dashboard'),
    path('owner/export/', views.export_appointments, name='export_appointments'),
    path('owner/edit/<int:id>/', views.edit_appointment, name='edit_appointment'),
    path('owner/delete/<int:id>/', views.delete_appointment, name='delete_appointment'),
    # Add other paths as needed
    # Include all app URLs here only if the app uses its own url configurations
    # path('', include('myapp.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
