from django.urls import path
from .views import home, about, register, login_view
from django.contrib.auth.views import LogoutView
from . import views  # Import views from the current app
from django.conf import settings
from django.conf.urls.static import static
from .views import book_appointment, appointment_list

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('appointment_list/', views.appointment_list, name='appointment_list'),
    path('appointment/cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('appointment/modify/<int:appointment_id>/', views.modify_appointment, name='modify_appointment'),
    path('api/events/', views.appointment_events, name='appointment_events'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
