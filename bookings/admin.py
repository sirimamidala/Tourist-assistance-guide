from django.contrib import admin
from .models import Service, Booking, LocalGuide, LocalGuideUpdate, ServiceRating

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price_per_unit', 'get_avg_rating', 'rating_count_display')
    list_filter = ('type',)
    search_fields = ('name',)

    def get_avg_rating(self, obj):
        avg = obj.avg_rating
        return f"{avg} ★" if avg else "No ratings"
    get_avg_rating.short_description = 'Avg Rating'

    def rating_count_display(self, obj):
        return obj.rating_count
    rating_count_display.short_description = 'Rating Count'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'guest_name', 'service', 'booking_date', 'status')
    list_filter = ('status', 'service__type')
    search_fields = ('user__username', 'guest_name', 'service__name')


@admin.register(LocalGuide)
class LocalGuideAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'location', 'approval_status', 'price_per_day', 'created_at')
    list_filter = ('approval_status', 'location')
    search_fields = ('full_name', 'user__username')
    
    actions = ['approve_guides', 'reject_guides']
    
    fieldsets = (
        ('User Info', {
            'fields': ('user', 'full_name')
        }),
        ('Personal Details', {
            'fields': ('location', 'languages_known', 'experience_years', 'specialization')
        }),
        ('Contact & Payment', {
            'fields': ('contact_number', 'price_per_day')
        }),
        ('Documents', {
            'fields': ('profile_photo', 'id_proof')
        }),
        ('Status', {
            'fields': ('approval_status',)
        }),
    )
    
    def approve_guides(self, request, queryset):
        from .models import Service
        for guide in queryset:
            guide.approval_status = 'APPROVED'
            
            # Create or update corresponding Service
            service_name = f"Guide: {guide.full_name}"
            service_desc = f"{guide.specialization} expert based in {guide.location}. {guide.experience_years} years of experience. Languages: {guide.languages_known}"
            
            if guide.service:
                service = guide.service
                service.name = service_name
                service.description = service_desc
                service.price_per_unit = guide.price_per_day
                service.contact_number = guide.contact_number
                if guide.profile_photo:
                    service.image = guide.profile_photo
                service.save()
            else:
                service = Service.objects.create(
                    type='GUIDE',
                    name=service_name,
                    description=service_desc,
                    price_per_unit=guide.price_per_day,
                    contact_number=guide.contact_number,
                    image=guide.profile_photo,
                    rating=5.0
                )
                guide.service = service
            
            guide.save()
            
        self.message_user(request, "Selected guides have been approved and listing services created/updated.")
    approve_guides.short_description = "Approve selected guides"
    
    def reject_guides(self, request, queryset):
        for guide in queryset:
            guide.approval_status = 'REJECTED'
            if guide.service:
                guide.service.delete()
                guide.service = None
            guide.save()
        self.message_user(request, "Selected guides have been rejected and their listings removed.")
    reject_guides.short_description = "Reject selected guides"


@admin.register(LocalGuideUpdate)
class LocalGuideUpdateAdmin(admin.ModelAdmin):
    list_display = ('guide', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('guide__full_name', 'guide__user__username')
    
    actions = ['approve_updates', 'reject_updates']
    
    def approve_updates(self, request, queryset):
        for update in queryset:
            if update.status == 'PENDING':
                guide = update.guide
                guide.full_name = update.full_name
                guide.location = update.location
                guide.languages_known = update.languages_known
                guide.experience_years = update.experience_years
                guide.price_per_day = update.price_per_day
                guide.contact_number = update.contact_number
                guide.specialization = update.specialization
                if update.profile_photo:
                    guide.profile_photo = update.profile_photo
                guide.save()
                
                update.status = 'APPROVED'
                update.save()
        self.message_user(request, "Selected updates have been approved and applied to guide profiles.")
    approve_updates.short_description = "Approve and Apply selected updates"
    
    def reject_updates(self, request, queryset):
        queryset.update(status='REJECTED')
        self.message_user(request, "Selected updates have been rejected.")
    reject_updates.short_description = "Reject selected updates"


@admin.register(ServiceRating)
class ServiceRatingAdmin(admin.ModelAdmin):
    list_display = ('service', 'user', 'rating', 'star_display', 'created_at')
    list_filter = ('rating', 'service')
    search_fields = ('user__username', 'service__name')
    readonly_fields = ('service', 'user', 'rating', 'created_at')

    def star_display(self, obj):
        return '★' * obj.rating + '☆' * (5 - obj.rating)
    star_display.short_description = 'Stars'

