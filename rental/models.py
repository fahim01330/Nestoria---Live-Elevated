from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
from django.db import models
from django.db.models import Q

class Profile(models.Model):
    OWNER = "owner"; 
    TENANT = "tenant"; 
    ROLE_CHOICES = [
        (OWNER, "Property Owner"),
        (TENANT, "Tenant")
    ]
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = "profile");
    role = models.CharField(max_length = 10, choices = ROLE_CHOICES, default = TENANT); 
    phone = models.CharField(max_length = 30, blank = True); 
    address = models.CharField(max_length = 255, blank = True)

    def __str__(self): 
        return f"{self.user.username} - {self.get_role_display()}"
    
class Property(models.Model):
    PROPERTY_TYPES = [
        ("Apartment", "Apartment"),
        ("House", "House"),
        ("Room", "Room"),
        ("Office", "Office")
    ]; 
    AVAILABILITY_CHOICES = [
        ("available", "Available"),
        ("rented", "Rented"),
        ("unavailable", "Unavailable")
    ]
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "properties"); 
    title = models.CharField(max_length = 200); 
    description = models.TextField(); 
    property_type = models.CharField(max_length = 20, choices = PROPERTY_TYPES); 
    location = models.CharField(max_length = 255); 
    monthly_rent = models.DecimalField(max_digits = 12, decimal_places = 2); 
    bedrooms = models.PositiveIntegerField(default = 1); 
    bathrooms = models.PositiveIntegerField(default = 1); 
    image = models.ImageField(upload_to = "properties/", blank = True, null = True); 
    availability_status = models.CharField(max_length = 20, choices = AVAILABILITY_CHOICES, default = "available");
    created_at = models.DateTimeField(auto_now_add = True); 
    updated_at = models.DateTimeField(auto_now = True)

    class Meta: 
        ordering = ["-created_at"]
    
    def __str__(self): 
        return self.title
    
class RentalRequest(models.Model):
    STATUS = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"), 
        ("cancelled", "Cancelled")
    ]
    property = models.ForeignKey(Property, on_delete = models.CASCADE, related_name = "rental_requests");
    tenant = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "rental_requests"); 
    message = models.TextField(); 
    request_date = models.DateTimeField(auto_now_add = True); 
    status = models.CharField(max_length = 20, choices = STATUS, default = "pending")

    class Meta:
        ordering=["-request_date"]
    
    constraints = [
        models.UniqueConstraint(fields = ["property", "tenant"],
        condition = Q(status = "pending"), 
        name = "unique_pending_request_per_tenant_property")
    ]
    
    def __str__(self): 
        return f"{self.tenant.username} -> {self.property.title}"

class Review(models.Model):
    property = models.ForeignKey(Property, on_delete = models.CASCADE, related_name = "reviews"); 
    tenant = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "reviews");
    rating = models.PositiveSmallIntegerField(validators = [
        MinValueValidator(1),
        MaxValueValidator(5)
    ]);
    comment = models.TextField();
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ["property", "tenant"],
            name="one_review_per_tenant_property")
        ]

    def __str__(self): 
        return f"{self.property.title} - {self.rating}/5"
