from django.urls import path
from . import views

urlpatterns = [
    # Main planner routes
    path('create/', views.create_plan_view, name='itinerary-create'),
    path('save/', views.save_plan_view, name='itinerary-save'),
    path('my/', views.my_itineraries_view, name='itinerary-list'),
    path('<int:pk>/', views.plan_detail_view, name='itinerary-detail'),
    path('<int:pk>/edit/', views.edit_plan_view, name='itinerary-edit'),
    path('<int:pk>/delete/', views.delete_plan_view, name='itinerary-delete'),
    path('<int:pk>/pdf/', views.download_pdf_view, name='itinerary-pdf'),

    # Legacy redirect alias (keep old URL working)
    path('plan/', views.create_plan_view, name='itinerary-planner'),
]
