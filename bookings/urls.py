from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:service_id>/', views.initiate_booking_view, name='initiate-booking'),
    path('checkout/<int:booking_id>/', views.checkout_session_view, name='checkout-session'),
    path('checkout/success/<int:booking_id>/', views.booking_success_view, name='booking-success'),
    path('guides/register/', views.guide_register_view, name='guide-register'),
    path('guides/pending/', views.guide_pending_view, name='guide-pending'),
    path('guides/<int:guide_id>/update/', views.guide_update_view, name='guide-update'),
    path('guides/<int:guide_id>/profile/', views.guide_profile_view, name='guide-profile'),
    path('guides/dashboard/', views.guide_dashboard_view, name='guide-dashboard'),
    path('guides/booking/<int:booking_id>/approve/', views.approve_booking_view, name='approve-booking'),
    path('guides/booking/<int:booking_id>/reject/', views.reject_booking_view, name='reject-booking'),
    path('services/<int:service_id>/rate/', views.rate_service_view, name='rate-service'),
]
