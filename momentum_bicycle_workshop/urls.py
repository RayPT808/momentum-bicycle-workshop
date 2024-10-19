from django.urls import path, include
from django.contrib import admin 
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('', include('myapp.urls')),
    # Add other paths as needed
]
