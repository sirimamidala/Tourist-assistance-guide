from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup_view, name='landing_signup'),
    path('home/', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('booking-system/', views.booking_system_view, name='booking-system'),
    path('community-feed/', views.community_feed_view, name='community-feed'),
    path('transport/', views.transport_view, name='transport'),
]
