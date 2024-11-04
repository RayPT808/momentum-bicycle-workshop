from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import home, about, register, login_view, book_appointment, appointment_list, appointment_events, profile, delete_appointment, modify_appointment
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('register/', register, name='register'),  # Directly use the imported function
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', profile, name='profile'),  # Directly use the imported function
    path('book/', book_appointment, name='book_appointment'),  # Directly use the imported function
    path('appointment_list/', appointment_list, name='appointment_list'),  # Directly use the imported function
    path('appointment/modify/<int:appointment_id>/', modify_appointment, name='modify_appointment'),  # Directly use the imported function
    path('delete/<int:id>/', delete_appointment, name='delete_appointment'),
    path('api/events/', appointment_events, name='appointment_events'),  # Directly use the imported function
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
