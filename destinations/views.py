from django.views.generic import ListView, DetailView
from tourist_project.services.weather_service import WeatherService
from .models import Destination

class DestinationListView(ListView):
    model = Destination
    template_name = 'destinations/list.html'
    context_object_name = 'destinations'

class DestinationDetailView(DetailView):
    model = Destination
    template_name = 'destinations/detail.html'
    context_object_name = 'destination'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attractions'] = self.object.attractions.all()
        context['weather'] = WeatherService.get_weather(self.object.location)
        return context
