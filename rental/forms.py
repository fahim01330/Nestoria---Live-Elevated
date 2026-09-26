from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Property, RentalRequest, Review

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs = {
            "placeholder": "name@example.com", 
            "class": "form-input"
        })
    )
    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        widget=forms.Select(attrs = {
            "class": "form-select"
        })
    )
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "+1 (555) 000-0000", "class": "form-input"})
    )
    address = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs = {
            "placeholder": "Miami, Florida", 
            "class": "form-input"
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "role", "phone", "address", "password1", "password2")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("role", "phone", "address")
        widgets = {
            "role": forms.Select(attrs = {"class": "form-select"}),
            "phone": forms.TextInput(attrs = {
                "placeholder": "+1 (555) 000-0000", 
                "class": "form-input"
            }),
            "address": forms.TextInput(attrs = {"placeholder": "e.g. 120 Ocean Dr, Miami, FL", "class": "form-input"}),
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Username", "class": "form-input"}),
            "first_name": forms.TextInput(attrs={"placeholder": "First Name", "class": "form-input"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name", "class": "form-input"}),
            "email": forms.EmailInput(attrs={"placeholder": "name@example.com", "class": "form-input"}),
        }

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = (
            "title", "description", "property_type", "location",
            "monthly_rent", "bedrooms", "bathrooms", "image", "availability_status"
        )
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g. Modern Ocean Villa", "class": "form-input"}),
            "location": forms.TextInput(attrs={"placeholder": "e.g. Miami, Florida", "class": "form-input"}),
            "monthly_rent": forms.NumberInput(attrs={"placeholder": "4200", "class": "form-input"}),
            "bedrooms": forms.NumberInput(attrs={"class": "form-input"}),
            "bathrooms": forms.NumberInput(attrs={"class": "form-input"}),
            "property_type": forms.Select(attrs={"class": "form-select"}),
            "availability_status": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "Describe the highlights and features...", "class": "form-input"}),
        }

class RentalRequestForm(forms.ModelForm):
    class Meta:
        model = RentalRequest
        fields = ("message",)
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4, "placeholder": "Introduce yourself and explain your lease requirements...", "class": "form-input"})
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("rating", "comment")
        widgets = {
            "rating": forms.Select(choices=[(i, f"{i} Stars ({i}/5)") for i in range(1, 6)], attrs={"class": "form-select"}),
            "comment": forms.Textarea(attrs={"rows": 4, "placeholder": "Share your experience with this property...", "class": "form-input"}),
        }
