from django.urls import path
from .views import AIAssistantView, EmergencyContactListView

urlpatterns = [
    path('emergency/', EmergencyContactListView.as_view(), name='emergency-help'),
    path('api/assistant/chat/', AIAssistantView.as_view(), name='ai-assistant'),
]
