from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from tourist_project.services.payment_service import PaymentService
from django.urls import reverse
from .models import Service, LocalGuide, Booking, LocalGuideUpdate, ServiceRating
from .forms import LocalGuideForm, BookingForm, LocalGuideUpdateForm
import datetime

@login_required
def initiate_booking_view(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.service = service
            booking.total_price = service.price_per_unit * form.cleaned_data['quantity']
            booking.status = 'WAITING_APPROVAL' if service.type == 'GUIDE' else 'PENDING'
            booking.save()
            
            # Redirect to checkout session
            return redirect('checkout-session', booking_id=booking.id)
    else:
        form = BookingForm(initial={'booking_date': datetime.date.today(), 'quantity': 1})
    
    return render(request, 'bookings/booking_form.html', {
        'form': form,
        'service': service
    })


@login_required
def checkout_session_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    service = booking.service
    
    success_url = request.build_absolute_uri(reverse('booking-success', kwargs={'booking_id': booking.id}))
    cancel_url = request.build_absolute_uri(reverse('booking-system')) + '?payment=cancelled'
    
    session_data = PaymentService.create_checkout_session(
        f"{service.name} (x{booking.quantity})",
        float(booking.total_price),
        success_url,
        cancel_url
    )
    
    if "url" in session_data:
        return redirect(session_data["url"])
    else:
        # Mock mode or error: redirect to success anyway to show flow
        return redirect(success_url)


@login_required
def booking_success_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.service.type != 'GUIDE':
        booking.status = 'CONFIRMED'
    booking.save()
    
    return render(request, 'bookings/success.html', {'booking': booking})


@login_required
def guide_register_view(request):
    # Multiple registrations allowed, no longer checking for existing guide OneToOne
    if request.method == 'POST':
        form = LocalGuideForm(request.POST, request.FILES)
        if form.is_valid():
            guide = form.save(commit=False)
            guide.user = request.user
            guide.approval_status = 'APPROVED'
            guide.save()
            
            # Automatically create a Service listing for this guide
            service = Service.objects.create(
                type='GUIDE',
                name=guide.full_name,
                description=f"Local guide specializing in: {guide.specialization or 'various areas'}. Experienced in {guide.location}.",
                price_per_unit=guide.price_per_day,
                contact_number=guide.contact_number,
                rating=5.0 # New guides start with a perfect rating
            )
            guide.service = service
            guide.save()
            
            return redirect(reverse('booking-system') + '?type=GUIDE')
    else:
        form = LocalGuideForm()
    
    return render(request, 'guides/register.html', {'form': form})


@login_required
def guide_pending_view(request):
    """Shows a pending review confirmation page after guide registration."""
    # Get the most recent guide registration for this user
    guide = request.user.local_guides.order_by('-created_at').first()
    if not guide:
        return redirect('guide-register')
    return render(request, 'guides/pending.html', {'guide': guide})


@login_required
def guide_update_view(request, guide_id):
    guide = get_object_or_404(LocalGuide, id=guide_id, user=request.user)
    
    # Check if there is already a pending update
    try:
        pending_update = guide.pending_update
    except LocalGuideUpdate.DoesNotExist:
        pending_update = None

    if request.method == 'POST':
        if pending_update:
            form = LocalGuideUpdateForm(request.POST, request.FILES, instance=pending_update)
        else:
            form = LocalGuideUpdateForm(request.POST, request.FILES)
            
        if form.is_valid():
            update = form.save(commit=False)
            update.guide = guide
            update.status = 'PENDING'
            update.save()
            return redirect('guide-profile', guide_id=guide.id)
    else:
        # Pre-fill with existing guide data if no pending update, 
        # or show the pending update data if it exists
        if pending_update:
            form = LocalGuideUpdateForm(instance=pending_update)
        else:
            form = LocalGuideUpdateForm(initial={
                'full_name': guide.full_name,
                'location': guide.location,
                'languages_known': guide.languages_known,
                'experience_years': guide.experience_years,
                'price_per_day': guide.price_per_day,
                'contact_number': guide.contact_number,
                'specialization': guide.specialization,
            })
    
    return render(request, 'guides/update.html', {'form': form, 'guide': guide})


@login_required
def guide_profile_view(request, guide_id):
    guide = get_object_or_404(LocalGuide, id=guide_id)
    
    # Check if logged-in user owns this guide profile
    if guide.user != request.user:
        # Unauthorized - show public profile or error
        return render(request, 'guides/profile.html', {
            'guide': guide, 
            'is_owner': False,
            'error': 'You can only view your own guide profile.'
        })
    
    # Check for pending update
    try:
        pending_update = guide.pending_update
    except LocalGuideUpdate.DoesNotExist:
        pending_update = None
        
    return render(request, 'guides/profile.html', {
        'guide': guide,
        'is_owner': True,
        'pending_update': pending_update
    })


@login_required
def guide_dashboard_view(request):
    """Dashboard for guides to manage their bookings."""
    # Get all guides owned by this user
    user_guides = request.user.local_guides.all()
    
    # Get all bookings linked to the services of these guides
    pending_requests = Booking.objects.filter(
        service__guide_listing__in=user_guides,
        status='WAITING_APPROVAL'
    ).order_by('-created_at')
    
    confirmed_bookings = Booking.objects.filter(
        service__guide_listing__in=user_guides,
        status='CONFIRMED'
    ).order_by('-created_at')
    
    return render(request, 'guides/dashboard.html', {
        'pending_requests': pending_requests,
        'confirmed_bookings': confirmed_bookings
    })


@login_required
def approve_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    # Check if the service has a guide listing and if the logged-in user owns it
    if hasattr(booking.service, 'guide_listing') and booking.service.guide_listing and booking.service.guide_listing.user == request.user:
        booking.status = 'CONFIRMED'
        booking.save()
    return redirect('guide-dashboard')


@login_required
def reject_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    # Check if the service has a guide listing and if the logged-in user owns it
    if hasattr(booking.service, 'guide_listing') and booking.service.guide_listing and booking.service.guide_listing.user == request.user:
        booking.status = 'REJECTED'
        booking.save()
    return redirect('guide-dashboard')


@login_required
def rate_service_view(request, service_id):
    """Accept a POST star rating (1-5) for a service and store it per user."""
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        try:
            rating_value = int(request.POST.get('rating', 0))
        except (ValueError, TypeError):
            rating_value = 0

        if 1 <= rating_value <= 5:
            ServiceRating.objects.update_or_create(
                service=service,
                user=request.user,
                defaults={'rating': rating_value}
            )

    # Redirect to the referring page (transport page) or default
    referer = request.META.get('HTTP_REFERER', '/transport/')
    return redirect(referer)
