from django.urls import path
from . import views  # Import views from the current app
from .views import register, book_appointment, appointment_list, home, profile 

urlpatterns = [
    path('', home, name='home'),
     path('about/', views.about, name='about'), 
    path('register/', register, name='register'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('accounts/profile/', profile, name='profile'), 
]



















"""
URL configuration for my_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""from django.contrib import admin
from django.urls import path, include
from workshop import views as index_views
from about import views as about_views

urlpatterns = [
    path('hello/', index_views.index, name='index'),
    path('about/', about_views.about_me, name='about'),
    path('admin/', admin.site.urls),
]
"""
