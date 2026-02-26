from django.contrib import admin
from .models import TouristPlace, TravelPlan, DayPlan, DayPlaceItem, TripBudget


@admin.register(TouristPlace)
class TouristPlaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'interest_category', 'budget_tier', 'estimated_cost', 'is_active']
    list_filter = ['interest_category', 'budget_tier', 'is_active']
    search_fields = ['name', 'location']
    list_editable = ['is_active']


class DayPlaceItemInline(admin.TabularInline):
    model = DayPlaceItem
    extra = 0


class DayPlanInline(admin.StackedInline):
    model = DayPlan
    extra = 0
    show_change_link = True


class TripBudgetInline(admin.StackedInline):
    model = TripBudget
    extra = 0
    readonly_fields = ('updated_at',)
    verbose_name = 'Budget Estimate'


@admin.register(TravelPlan)
class TravelPlanAdmin(admin.ModelAdmin):
    list_display = ['destination', 'user', 'num_days', 'budget', 'start_date', 'end_date', 'created_at']
    list_filter = ['budget']
    search_fields = ['destination', 'user__username']
    inlines = [DayPlanInline, TripBudgetInline]


@admin.register(DayPlan)
class DayPlanAdmin(admin.ModelAdmin):
    list_display = ['travel_plan', 'day_number']
    inlines = [DayPlaceItemInline]


@admin.register(DayPlaceItem)
class DayPlaceItemAdmin(admin.ModelAdmin):
    list_display = ['place', 'day_plan', 'order']


@admin.register(TripBudget)
class TripBudgetAdmin(admin.ModelAdmin):
    list_display = ['plan', 'hotel_cost', 'transport_cost', 'food_cost', 'get_total', 'updated_at']
    search_fields = ['plan__destination', 'plan__user__username']
    readonly_fields = ('updated_at',)

    def get_total(self, obj):
        return f"₹{obj.total_cost}"
    get_total.short_description = 'Total Cost'

