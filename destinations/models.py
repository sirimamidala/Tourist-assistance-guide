from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Destination(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='destinations/')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Attraction(models.Model):
    CATEGORY_CHOICES = (
        ('HISTORICAL', 'Historical Site'),
        ('NATURE', 'Nature'),
        ('ADVENTURE', 'Adventure'),
        ('CULTURAL', 'Cultural Event'),
    )
    destination = models.ForeignKey(Destination, related_name='attractions', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    photo = models.ImageField(upload_to='attractions/', blank=True, null=True)
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.name} ({self.destination.name})"

class Gallery(models.Model):
    destination = models.ForeignKey(Destination, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Gallery for {self.destination.name}"
