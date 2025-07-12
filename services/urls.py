from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.service_list, name='service_list'),
    path('services/<slug:category_slug>/', views.service_list, name='service_list_by_category'),
    path('book/<slug:slug>/', views.book_service, name='book_service'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    
    # Admin response URL (only include if you implemented the view)
    path('admin/response/<int:booking_id>/', views.admin_response, name='admin_response'),
]