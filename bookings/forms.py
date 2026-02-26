from django import forms
from .models import Service, LocalGuide, Booking, LocalGuideUpdate


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'type', 'description', 'price_per_unit', 'image']


class LocalGuideForm(forms.ModelForm):
    class Meta:
        model = LocalGuide
        fields = ['full_name', 'location', 'languages_known', 'experience_years', 
                  'price_per_day', 'contact_number', 'profile_photo', 'id_proof', 'specialization']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City/State'}),
            'languages_known': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., English, Telugu, Hindi'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Years of Experience'}),
            'price_per_day': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price per Day'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Contact Number'}),
            'profile_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'id_proof': forms.FileInput(attrs={'class': 'form-control'}),
            'specialization': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'e.g., Temples, Historical places, Adventure trips'}),
        }


class LocalGuideUpdateForm(forms.ModelForm):
    class Meta:
        model = LocalGuideUpdate
        fields = ['full_name', 'location', 'languages_known', 'experience_years', 
                  'price_per_day', 'contact_number', 'profile_photo', 'specialization']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'languages_known': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_per_day': forms.NumberInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'specialization': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['guest_name', 'booking_date', 'quantity', 'pickup_location', 'drop_location']
        widgets = {
            'guest_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., John Doe (Optional)'}),
            'booking_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'pickup_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter pickup address'}),
            'drop_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter destination address'}),
        }