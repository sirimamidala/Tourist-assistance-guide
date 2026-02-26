from django.db import models


class Place(models.Model):
    CATEGORY_CHOICES = [
        ('BEACH', 'Beach'),
        ('HILL_STATION', 'Hill Station'),
        ('HISTORICAL', 'Historical Place'),
        ('NATURE', 'Nature / Wildlife'),
        ('ADVENTURE', 'Adventure'),
        ('CITY', 'City / Urban'),
        ('OTHER', 'Other'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='OTHER')
    image = models.ImageField(upload_to='explorer/')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class HillStation(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='India')
    description = models.TextField()
    best_time_to_visit = models.CharField(max_length=200, help_text="e.g., April-June")
    temperature_range = models.CharField(max_length=100, help_text="e.g., 10°C - 25°C")
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(upload_to='explorer/hill_stations/')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']
        verbose_name = "Hill Station"
        verbose_name_plural = "Hill Stations"

    def __str__(self):
        return f"{self.name} - {self.city}, {self.state}"
