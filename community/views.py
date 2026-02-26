from django.views.generic import ListView
from rest_framework import views
from rest_framework.response import Response
from .models import EmergencyContact

class AIAssistantView(views.APIView):
    def post(self, request):
        question = request.data.get('question', '')
        # Mock AI logic
        response_text = f"As your AI Tourist Assistant, here's a tip for '{question}': Always carry a local map and check weather updates before heading to nature attractions! How else can I help?"
        return Response({"answer": response_text})

class EmergencyContactListView(ListView):
    model = EmergencyContact
    template_name = 'community/emergency.html'
    context_object_name = 'contacts'
