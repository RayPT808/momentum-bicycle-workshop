from django.urls import path, include
from django.contrib import admin
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import CustomLogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),  # Include app-level URLs
    path('owner/dashboard/', views.OwnerDashboardView.as_view(), name='owner_dashboard'),
    path('owner/export/', views.export_appointments, name='export_appointments'),
    path('owner/edit/<int:id>/', views.edit_appointment, name='edit_appointment'),
    path('owner/delete/<int:id>/', views.delete_appointment, name='delete_appointment'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
