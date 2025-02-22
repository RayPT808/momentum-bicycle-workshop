from django.urls import path
from . import views
from .views import home, about, register, login_view, book_appointment, appointment_list, appointment_events, profile, delete_appointment, modify_appointment
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('profile/', profile, name='profile'),
    path('book/', book_appointment, name='book_appointment'),
    path('appointment_list/', appointment_list, name='appointment_list'),
    path('appointment/modify/<int:appointment_id>/', modify_appointment, name='modify_appointment'),
    path('delete/<int:id>/', delete_appointment, name='delete_appointment'),
    path('api/events/', appointment_events, name='appointment_events'),
    path('owner/appointments/mark_completed/<int:appointment_id>/', views.mark_appointment_completed, name='mark_completed'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
