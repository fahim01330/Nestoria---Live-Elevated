from django.contrib import admin
from .models import Profile, Property, RentalRequest, Review

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin): 
    list_display = ("user", "role", "phone"); 
    list_filter = ("role",); 
    search_fields = ("user__username", "phone")

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin): 
    list_display = ("title", "owner", "property_type", "location", "monthly_rent", "availability_status"); 
    list_filter = ("property_type", "availability_status");
    search_fields=("title", "location", "owner__username"); 
    list_select_related=("owner",)

@admin.register(RentalRequest)
class RentalRequestAdmin(admin.ModelAdmin): 
    list_display = ("property", "tenant", "status", "request_date");
    list_filter = ("status",); 
    search_fields = ("property__title", "tenant__username");
    list_select_related = ("property", "tenant")

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin): 
    list_display = ("property", "tenant", "rating", "created_at"); 
    list_filter = ("rating", ); 
    search_fields = ("property__title", "tenant__username");
    list_select_related = ("property", "tenant")
