from django.shortcuts import render, redirect
from bookings.models import Service, ServiceRating
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect("login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = SignupForm()
    return render(request, "accounts/signup.html", {"signup_form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Welcome back, {username}! Your details have been verified against our database.")
                return redirect("profile")
            else:
                messages.error(request, "Incorrect details")
        else:
            messages.error(request, "Incorrect details")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"login_form": form})

@login_required
def profile_view(request):
    return render(request, "accounts/profile.html")

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")

@login_required
def home_view(request):
    show_profile = request.GET.get('show_profile') == 'true'
    return render(request, "home.html", {"show_profile": show_profile})

@login_required
def dashboard_view(request):
    from bookings.models import Booking
    recent_bookings = Booking.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, "accounts/dashboard.html", {"recent_bookings": recent_bookings})

@login_required
def booking_system_view(request):
    service_type = request.GET.get('type', None)
    
    if service_type == 'GUIDE':
        # Show approved local guides
        from bookings.models import LocalGuide
        guides = LocalGuide.objects.filter(approval_status='APPROVED')
        return render(request, "booking_system_guides.html", {"guides": guides, "active_type": service_type})
    elif service_type:
        services = Service.objects.filter(type=service_type)
    else:
        services = Service.objects.all()
    
    return render(request, "booking_system.html", {"services": services, "active_type": service_type})

@login_required
def community_feed_view(request):
    return render(request, "community_feed.html")

@login_required
def transport_view(request):
    transport_services = list(Service.objects.filter(type='TRANSPORT'))

    # Annotate each service with the logged-in user's submitted rating (or 0)
    if request.user.is_authenticated:
        existing = {
            r['service_id']: r['rating']
            for r in ServiceRating.objects.filter(
                user=request.user,
                service__in=transport_services
            ).values('service_id', 'rating')
        }
        for svc in transport_services:
            svc.user_rating = existing.get(svc.id, 0)
    else:
        for svc in transport_services:
            svc.user_rating = 0

    return render(request, "transport.html", {
        "services": transport_services,
    })


