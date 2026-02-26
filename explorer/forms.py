from django import forms
from .models import Place, HillStation


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['name', 'description', 'location', 'category', 'image', 'latitude', 'longitude']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Goa Beaches'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write a detailed description...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Goa, India'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 15.2993',
                'step': '0.0001'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 73.8243',
                'step': '0.0001'
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class GeoLocationSearchForm(forms.Form):
    PLACE_TYPE_CHOICES = [
        ('HOTEL', 'Hotel'),
        ('HOSPITAL', 'Hospital'),
        ('TEMPLE', 'Temple'),
        ('ATTRACTION', 'Tourist Attraction'),
        ('RESTAURANT', 'Restaurant'),
        ('BEACH', 'Beach'),
        ('HILL_STATION', 'Hill Station'),
        ('HISTORICAL', 'Historical Place'),
        ('NATURE', 'Nature / Wildlife'),
        ('ADVENTURE', 'Adventure'),
        ('CITY', 'City / Urban'),
    ]
    
    RADIUS_CHOICES = [
        (1, '1 km'),
        (5, '5 km'),
        (10, '10 km'),
        (25, '25 km'),
        (50, '50 km'),
    ]
    
    location_name = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter city or location name',
            'id': 'location-input'
        })
    )
    latitude = forms.FloatField(
        required=False,
        widget=forms.HiddenInput()
    )
    longitude = forms.FloatField(
        required=False,
        widget=forms.HiddenInput()
    )
    place_type = forms.ChoiceField(
        choices=[('', '-- Select place type --')] + PLACE_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    search_radius = forms.ChoiceField(
        choices=RADIUS_CHOICES,
        initial=50,
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class HillStationForm(forms.ModelForm):
    class Meta:
        model = HillStation
        fields = ['name', 'city', 'district', 'state', 'country', 'description', 
                  'best_time_to_visit', 'temperature_range', 'latitude', 'longitude', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Shimla'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Shimla'
            }),
            'district': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Shimla'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Himachal Pradesh'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. India',
                'value': 'India'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write a detailed description...'
            }),
            'best_time_to_visit': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. April-June'
            }),
            'temperature_range': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 10°C - 25°C'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 31.7683',
                'step': '0.0001'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 77.1092',
                'step': '0.0001'
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
