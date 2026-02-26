from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    SERVICE_TYPES = (
        ('HOTEL', 'Hotel'),
        ('RESTAURANT', 'Restaurant'),
        ('TRANSPORT', 'Transport'),
        ('GUIDE', 'Local Guide'),
    )
    TRANSPORT_CATEGORIES = (
        ('CAB', 'Cabs / Taxis'),
        ('BUS', 'Buses'),
        ('TRAIN', 'Trains'),
        ('FLIGHT', 'Flights'),
        ('CAR_RENTAL', 'Car Rentals'),
        ('BIKE_RENTAL', 'Bike Rentals'),
    )

    type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    availability_calendar = models.JSONField(default=dict, help_text="Store availability as date strings")
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    
    # Transport specific fields
    transport_category = models.CharField(max_length=20, choices=TRANSPORT_CATEGORIES, blank=True, null=True)
    pickup_location = models.CharField(max_length=200, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    rating = models.FloatField(default=0.0)  # legacy field kept for backwards compat

    def __str__(self):
        return f"{self.get_type_display()}: {self.name}"

    @property
    def avg_rating(self):
        """Compute live average from user-submitted ServiceRating rows."""
        from django.db.models import Avg
        result = self.service_ratings.aggregate(avg=Avg('rating'))['avg']
        return round(result, 1) if result else None

    @property
    def rating_count(self):
        """Total number of user-submitted ratings."""
        return self.service_ratings.count()

class Booking(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('WAITING_APPROVAL', 'Waiting for Approval'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('REJECTED', 'Rejected'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=200, blank=True, null=True, help_text="Primary guest name (optional)")
    booking_date = models.DateField()
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    pickup_location = models.CharField(max_length=200, blank=True, null=True)
    drop_location = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} - {self.user.username}"


class LocalGuide(models.Model):
    APPROVAL_STATUS = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='local_guides')
    service = models.OneToOneField(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='guide_listing')
    full_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, help_text="City/State")
    languages_known = models.CharField(max_length=500, help_text="Comma-separated languages")
    experience_years = models.PositiveIntegerField(help_text="Years of experience")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    contact_number = models.CharField(max_length=20)
    profile_photo = models.ImageField(upload_to='guides/profiles/', blank=True, null=True)
    id_proof = models.FileField(upload_to='guides/id_proofs/', blank=True, null=True)
    approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS, default='APPROVED')
    specialization = models.CharField(max_length=500, blank=True, null=True, help_text="Areas of expertise")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.location}"


class LocalGuideUpdate(models.Model):
    APPROVAL_STATUS = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )
    
    guide = models.OneToOneField(LocalGuide, on_delete=models.CASCADE, related_name='pending_update')
    full_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    languages_known = models.CharField(max_length=500)
    experience_years = models.PositiveIntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    contact_number = models.CharField(max_length=20)
    profile_photo = models.ImageField(upload_to='guides/profiles/', blank=True, null=True)
    specialization = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=20, choices=APPROVAL_STATUS, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Update for {self.guide.full_name} - {self.status}"


class ServiceRating(models.Model):
    """A user-submitted star rating for a transport service."""
    STAR_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='service_ratings'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='service_ratings'
    )
    rating = models.IntegerField(choices=STAR_CHOICES)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('service', 'user')  # one rating per user per service

    def __str__(self):
        return f"{self.user.username} rated {self.service.name}: {self.rating}★"
