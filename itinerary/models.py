from django.db import models
from django.contrib.auth.models import User


INTEREST_CHOICES = [
    ('temples', 'Temples'),
    ('adventure', 'Adventure'),
    ('hill_stations', 'Hill Stations'),
    ('food', 'Food & Cuisine'),
    ('shopping', 'Shopping'),
    ('beaches', 'Beaches'),
    ('historical', 'Historical Places'),
    ('nature', 'Nature & Wildlife'),
]

BUDGET_CHOICES = [
    ('economy', 'Economy (₹0 – ₹500/day)'),
    ('moderate', 'Moderate (₹500 – ₹2000/day)'),
    ('luxury', 'Luxury (₹2000+/day)'),
]


class TouristPlace(models.Model):
    """A tourist place that can be recommended in itineraries."""
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    interest_category = models.CharField(
        max_length=20, choices=INTEREST_CHOICES, default='nature'
    )
    budget_tier = models.CharField(
        max_length=10, choices=BUDGET_CHOICES, default='moderate'
    )
    estimated_cost = models.PositiveIntegerField(
        help_text='Estimated cost per person in INR', default=0
    )
    image = models.ImageField(upload_to='itinerary/places/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, help_text='External image URL fallback')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Tourist Place'
        verbose_name_plural = 'Tourist Places'

    def __str__(self):
        return f"{self.name} — {self.location} [{self.interest_category}]"

    def get_image(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return None


class TravelPlan(models.Model):
    """A user's saved travel plan / itinerary."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='travel_plans')
    destination = models.CharField(max_length=200)
    num_days = models.PositiveIntegerField(default=1)
    budget = models.CharField(max_length=10, choices=BUDGET_CHOICES, default='moderate')
    start_date = models.DateField()
    end_date = models.DateField()
    interests = models.CharField(
        max_length=500, blank=True,
        help_text='Comma-separated list of interest values'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Travel Plan'

    def __str__(self):
        return f"{self.destination} ({self.num_days} days) — {self.user.username}"

    def get_interests_list(self):
        if self.interests:
            return [i.strip() for i in self.interests.split(',') if i.strip()]
        return []

    def get_interests_display(self):
        mapping = dict(INTEREST_CHOICES)
        return ', '.join(mapping.get(i, i) for i in self.get_interests_list())

    def get_budget_display_label(self):
        mapping = dict(BUDGET_CHOICES)
        return mapping.get(self.budget, self.budget)


class DayPlan(models.Model):
    """One day within a TravelPlan."""
    travel_plan = models.ForeignKey(TravelPlan, on_delete=models.CASCADE, related_name='day_plans')
    day_number = models.PositiveIntegerField()

    class Meta:
        ordering = ['day_number']
        verbose_name = 'Day Plan'

    def __str__(self):
        return f"Day {self.day_number} of {self.travel_plan}"


class DayPlaceItem(models.Model):
    """A tourist place assigned to a particular day."""
    day_plan = models.ForeignKey(DayPlan, on_delete=models.CASCADE, related_name='place_items')
    place = models.ForeignKey(TouristPlace, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Day Place Item'

    def __str__(self):
        return f"{self.place.name} — Day {self.day_plan.day_number}"


class TripBudget(models.Model):
    """Estimated budget breakdown for a TravelPlan."""
    plan = models.OneToOneField(
        TravelPlan,
        on_delete=models.CASCADE,
        related_name='budget_estimate'
    )
    hotel_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        help_text="Estimated hotel/accommodation cost in ₹"
    )
    transport_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        help_text="Estimated transportation cost in ₹"
    )
    food_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        help_text="Estimated food & dining cost in ₹"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Trip Budget'
        verbose_name_plural = 'Trip Budgets'

    def __str__(self):
        return f"Budget for {self.plan} — ₹{self.total_cost}"

    @property
    def total_cost(self):
        return (self.hotel_cost or 0) + (self.transport_cost or 0) + (self.food_cost or 0)
