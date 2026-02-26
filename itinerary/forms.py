from django import forms
from .models import TravelPlan, TripBudget, INTEREST_CHOICES, BUDGET_CHOICES


class TravelPlanForm(forms.ModelForm):
    interests = forms.MultipleChoiceField(
        choices=INTEREST_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Your Interests',
        error_messages={'required': 'Please select at least one interest.'}
    )

    class Meta:
        model = TravelPlan
        fields = ['destination', 'num_days', 'budget', 'start_date', 'end_date']
        widgets = {
            'destination': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Hyderabad, Goa, Manali',
                'autocomplete': 'off',
            }),
            'num_days': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 30,
            }),
            'budget': forms.RadioSelect(attrs={'class': 'btn-check'}),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }
        labels = {
            'destination': 'Destination',
            'num_days': 'Number of Days',
            'budget': 'Budget Range',
            'start_date': 'Start Date',
            'end_date': 'End Date',
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        num_days = cleaned_data.get('num_days')

        if start and end:
            if end < start:
                raise forms.ValidationError('End date must be after start date.')
            delta = (end - start).days + 1
            if num_days and num_days > delta:
                raise forms.ValidationError(
                    f'Number of days ({num_days}) cannot exceed the date range ({delta} days).'
                )
        return cleaned_data

    def clean_interests(self):
        interests = self.cleaned_data.get('interests', [])
        if not interests:
            raise forms.ValidationError('Please select at least one interest.')
        return ','.join(interests)


class BudgetForm(forms.ModelForm):
    class Meta:
        model = TripBudget
        fields = ['hotel_cost', 'transport_cost', 'food_cost']
        widgets = {
            'hotel_cost': forms.NumberInput(attrs={
                'class': 'form-control budget-input',
                'placeholder': '0.00',
                'min': '0',
                'step': '0.01',
                'id': 'id_hotel_cost',
            }),
            'transport_cost': forms.NumberInput(attrs={
                'class': 'form-control budget-input',
                'placeholder': '0.00',
                'min': '0',
                'step': '0.01',
                'id': 'id_transport_cost',
            }),
            'food_cost': forms.NumberInput(attrs={
                'class': 'form-control budget-input',
                'placeholder': '0.00',
                'min': '0',
                'step': '0.01',
                'id': 'id_food_cost',
            }),
        }
        labels = {
            'hotel_cost': '🏨 Hotel / Accommodation Cost (₹)',
            'transport_cost': '🚗 Transportation Cost (₹)',
            'food_cost': '🍽️ Food & Dining Cost (₹)',
        }
