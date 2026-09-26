from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    # Home & Search
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),

    # Authentication
    path("register/", views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="rental/login.html"
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),

    # User
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile_update, name="profile"),
    path("profile/update/", views.profile_update, name="profile_update"),
    path("profile/edit/", views.profile_update, name="profile_edit"),

    # Owner - Property
    path(
        "owner/property/add/",
        views.property_create,
        name="property_create",
    ),
    path(
        "owner/property/<int:pk>/edit/",
        views.property_update,
        name="property_update",
    ),
    path(
        "owner/property/<int:pk>/delete/",
        views.property_delete,
        name="property_delete",
    ),

    # Owner - Rental Request
    path(
        "owner/request/<int:pk>/<str:action>/",
        views.owner_request_action,
        name="owner_request_action",
    ),

    # Property Details
    path(
        "property/<int:pk>/",
        views.property_detail,
        name="property_detail",
    ),

    # Tenant - Rental Request
    path(
        "tenant/property/<int:pk>/request/",
        views.rental_request_create,
        name="rental_request_create",
    ),
    path(
        "tenant/request/<int:pk>/cancel/",
        views.rental_request_cancel,
        name="rental_request_cancel",
    ),

    # Reviews
    path(
        "property/<int:pk>/review/",
        views.review_create,
        name="review_create",
    ),
]