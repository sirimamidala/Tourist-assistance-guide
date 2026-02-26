import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from .models import TouristPlace, TravelPlan, DayPlan, DayPlaceItem, INTEREST_CHOICES, BUDGET_CHOICES
from .forms import TravelPlanForm, BudgetForm


PLACES_PER_DAY = 2


def _get_budget_tiers(budget):
    """Return the list of budget tiers to include for a given selection."""
    if budget == 'economy':
        return ['economy']
    elif budget == 'moderate':
        return ['economy', 'moderate']
    else:  # luxury
        return ['economy', 'moderate', 'luxury']


def _distribute_places(places, num_days):
    """Distribute a queryset of places into a list of day-lists."""
    places = list(places)
    random.shuffle(places)
    days = []
    for day in range(num_days):
        start = day * PLACES_PER_DAY
        end = start + PLACES_PER_DAY
        day_places = places[start:end]
        if day_places:
            days.append({'day_number': day + 1, 'places': day_places})
    return days


@login_required
def create_plan_view(request):
    """Show the preference form; on POST generate a day-wise plan preview."""
    generated_days = None
    form = TravelPlanForm()
    budget_form = BudgetForm()

    if request.method == 'POST':
        form = TravelPlanForm(request.POST)
        budget_form = BudgetForm(request.POST)

        if form.is_valid() and budget_form.is_valid():
            destination = form.cleaned_data['destination']
            num_days = form.cleaned_data['num_days']
            budget = form.cleaned_data['budget']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            # interests stored as comma-separated string by the form's clean_interests
            interests_str = form.cleaned_data['interests']
            interest_list = [i.strip() for i in interests_str.split(',') if i.strip()]

            # Store budget data in session
            request.session['pending_budget'] = {
                'hotel_cost': str(budget_form.cleaned_data['hotel_cost']),
                'transport_cost': str(budget_form.cleaned_data['transport_cost']),
                'food_cost': str(budget_form.cleaned_data['food_cost']),
            }
            # Filter places by interests (OR) and budget
            tiers = _get_budget_tiers(budget)
            places_qs = TouristPlace.objects.filter(
                interest_category__in=interest_list,
                budget_tier__in=tiers,
                is_active=True,
            )

            total_needed = num_days * PLACES_PER_DAY
            if places_qs.count() == 0:
                messages.warning(
                    request,
                    'No places found for your selected interests and budget. '
                    'Showing all available places instead.'
                )
                places_qs = TouristPlace.objects.filter(is_active=True)

            generated_days = _distribute_places(places_qs, num_days)

            # Store generation context in session for saving
            request.session['pending_plan'] = {
                'destination': destination,
                'num_days': num_days,
                'budget': budget,
                'start_date': str(start_date),
                'end_date': str(end_date),
                'interests': interests_str,
                'day_place_ids': [
                    [p.id for p in day['places']] for day in generated_days
                ],
            }

            return render(request, 'itinerary/plan_result.html', {
                'generated_days': generated_days,
                'form_data': {
                    'destination': destination,
                    'num_days': num_days,
                    'budget': budget,
                    'start_date': start_date,
                    'end_date': end_date,
                    'interests': interests_str,
                },
            })

    return render(request, 'itinerary/plan_form.html', {'form': form, 'budget_form': budget_form})


@login_required
def save_plan_view(request):
    """Save the pending generated plan to the database."""
    if request.method != 'POST':
        return redirect('itinerary-create')

    pending = request.session.get('pending_plan')
    if not pending:
        messages.error(request, 'No plan to save. Please generate a plan first.')
        return redirect('itinerary-create')

    # Create TravelPlan
    plan = TravelPlan.objects.create(
        user=request.user,
        destination=pending['destination'],
        num_days=pending['num_days'],
        budget=pending['budget'],
        start_date=pending['start_date'],
        end_date=pending['end_date'],
        interests=pending['interests'],
    )

    # Create TripBudget if budget data was provided
    pending_budget = request.session.pop('pending_budget', None)
    if pending_budget:
        TripBudget.objects.create(
            plan=plan,
            hotel_cost=pending_budget.get('hotel_cost', 0),
            transport_cost=pending_budget.get('transport_cost', 0),
            food_cost=pending_budget.get('food_cost', 0),
        )

    for day_idx, place_ids in enumerate(pending['day_place_ids'], start=1):
        day_plan = DayPlan.objects.create(travel_plan=plan, day_number=day_idx)
        for order, place_id in enumerate(place_ids):
            try:
                place = TouristPlace.objects.get(id=place_id)
                DayPlaceItem.objects.create(day_plan=day_plan, place=place, order=order)
            except TouristPlace.DoesNotExist:
                pass

    # Clear session
    del request.session['pending_plan']
    messages.success(request, f'Itinerary for {plan.destination} saved successfully! ✅')
    return redirect('itinerary-detail', pk=plan.pk)


@login_required
def my_itineraries_view(request):
    """List all travel plans for the logged-in user."""
    plans = TravelPlan.objects.filter(user=request.user).prefetch_related(
        'day_plans__place_items__place'
    )
    return render(request, 'itinerary/my_itineraries.html', {'plans': plans})


@login_required
def plan_detail_view(request, pk):
    """View a saved travel plan in detail."""
    plan = get_object_or_404(TravelPlan, pk=pk, user=request.user)
    day_plans = plan.day_plans.prefetch_related('place_items__place').all()
    
    # Try to get existing budget or None
    try:
        budget_obj = plan.budget_estimate
    except TripBudget.DoesNotExist:
        budget_obj = None

    return render(request, 'itinerary/plan_detail.html', {
        'plan': plan,
        'day_plans': day_plans,
        'budget': budget_obj,
    })


@login_required
def edit_plan_view(request, pk):
    """Edit a saved travel plan and its budget."""
    plan = get_object_or_404(TravelPlan, pk=pk, user=request.user)
    
    # Get or create budget instance
    budget_instance, created = TripBudget.objects.get_or_create(plan=plan)

    interest_list = plan.get_interests_list()

    if request.method == 'POST':
        form = TravelPlanForm(request.POST, instance=plan)
        budget_form = BudgetForm(request.POST, instance=budget_instance)
        
        if form.is_valid() and budget_form.is_valid():
            form.save()
            budget_form.save()
            messages.success(request, 'Itinerary and budget updated successfully! ✅')
            return redirect('itinerary-detail', pk=plan.pk)
    else:
        initial_data = {'interests': interest_list}
        form = TravelPlanForm(instance=plan, initial=initial_data)
        budget_form = BudgetForm(instance=budget_instance)

    return render(request, 'itinerary/edit_plan.html', {
        'form': form, 
        'budget_form': budget_form,
        'plan': plan
    })


@login_required
def delete_plan_view(request, pk):
    """Delete a travel plan."""
    plan = get_object_or_404(TravelPlan, pk=pk, user=request.user)
    if request.method == 'POST':
        destination = plan.destination
        plan.delete()
        messages.success(request, f'Itinerary for {destination} deleted.')
        return redirect('itinerary-list')
    return render(request, 'itinerary/delete_confirm.html', {'plan': plan})


@login_required
def download_pdf_view(request, pk):
    """Generate and download a PDF version of a travel plan."""
    plan = get_object_or_404(TravelPlan, pk=pk, user=request.user)
    day_plans = plan.day_plans.prefetch_related('place_items__place').all()

    template = get_template('itinerary/pdf_template.html')
    html = template.render({'plan': plan, 'day_plans': day_plans, 'request': request})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="itinerary_{plan.destination}_{plan.id}.pdf"'

    try:
        from xhtml2pdf import pisa
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Error generating PDF', status=500)
    except ImportError:
        return HttpResponse(
            'PDF library not installed. Please run: pip install xhtml2pdf',
            status=500
        )

    return response
