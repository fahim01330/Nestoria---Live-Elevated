from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Avg,Count,Q
from django.shortcuts import get_object_or_404,redirect,render
from .forms import *
from .models import *

def home(request):
    qs = Property.objects.filter(availability_status="available").select_related("owner").annotate(
        review_count=Count("reviews"),
        average_rating=Avg("reviews__rating")
    )
    loc = request.GET.get("location", "").strip()
    typ = request.GET.get("property_type", "").strip()
    mn = request.GET.get("min_rent", "")
    mx = request.GET.get("max_rent", "")
    price_range = request.GET.get("price_range", "").strip()

    if price_range:
        if price_range == "1000-5000":
            mn, mx = 1000, 5000
        elif price_range == "under-1000":
            mx = 1000
        elif price_range == "5000-plus":
            mn = 5000
        elif "-" in price_range:
            parts = price_range.split("-")
            if len(parts) == 2:
                try:
                    mn, mx = float(parts[0]), float(parts[1])
                except ValueError:
                    pass

    if loc:
        qs = qs.filter(location__icontains=loc)
    if typ and typ != "Any Type" and typ != "all":
        qs = qs.filter(property_type__iexact=typ)
    if mn:
        try:
            qs = qs.filter(monthly_rent__gte=float(mn))
        except (ValueError, TypeError):
            pass
    if mx:
        try:
            qs = qs.filter(monthly_rent__lte=float(mx))
        except (ValueError, TypeError):
            pass
            
    return render(request, "rental/home.html", {
        "properties": qs,
        "property_types": Property.PROPERTY_TYPES,
        "filters": request.GET,
    })

def property_detail(request,pk):
    p = get_object_or_404(Property.objects.select_related("owner").prefetch_related("reviews__tenant"), pk = pk); 
    reviews = p.reviews.all(); 
    avg = reviews.aggregate(avg=Avg("rating"))["avg"];
    can_review = False

    if request.user.is_authenticated: 
        can_review = RentalRequest.objects.filter(property = p, tenant = request.user, status = "accepted").exists() and not Review.objects.filter(property=p,tenant=request.user).exists()

    return render(request, "rental/property_detail.html", {
        "property": p,
        "reviews": reviews,
        "average_rating": avg,
        "can_review": can_review
    })

def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    
    f = RegisterForm(request.POST or None)
    
    if request.method=="POST" and f.is_valid():
        u = f.save();
        Profile.objects.create(user = u, role = f.cleaned_data["role"], phone = f.cleaned_data["phone"], address = f.cleaned_data["address"]);
        login(request,u);
        return redirect("dashboard")
    
    return render(request, "rental/register.html", {"form": f})

@login_required
def dashboard(request):
    role=request.user.profile.role

    if role=="owner":
        props=Property.objects.filter(owner=request.user); reqs=RentalRequest.objects.filter(property__owner=request.user)
        c = {
            "role": "owner",
            "properties": props,
            "requests": reqs.select_related("property","tenant")[:20],
            "total_properties": props.count(),
            "available_properties": props.filter(availability_status="available").count(),
            "total_requests": reqs.count(),
            "pending_requests": reqs.filter(status="pending").count(),
            "accepted_requests": reqs.filter(status="accepted").count()
        }
    else:
        reqs = RentalRequest.objects.filter(tenant=request.user); 
        c = {
            "role": "tenant",
            "requests": reqs.select_related("property")[:20],
            "total_requests": reqs.count(),
            "pending_requests": reqs.filter(status="pending").count(),
            "accepted_requests": reqs.filter(status="accepted").count(),
            "rejected_requests": reqs.filter(status="rejected").count()
        }

    return render(request, "rental/dashboard.html", c)

@login_required
def profile_update(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        uf = UserUpdateForm(request.POST, instance=request.user)
        pf = ProfileForm(request.POST, instance=profile_obj)
        if uf.is_valid() and pf.is_valid():
            uf.save()
            pf.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("profile")
    else:
        uf = UserUpdateForm(instance=request.user)
        pf = ProfileForm(instance=profile_obj)
    
    return render(request, "rental/profile.html", {
        "user_form": uf,
        "profile_form": pf
    })

profile = profile_update

@login_required
def property_create(request):
    if request.user.profile.role!="owner": 
        return redirect("dashboard")
    
    f = PropertyForm(request.POST or None, request.FILES or None)
    
    if request.method == "POST" and f.is_valid(): 
        p = f.save(commit=False);
        p.owner = request.user;
        p.save();
        return redirect("dashboard")

    return render(request,"rental/form.html",{"form":f,"title":"Add Property"})

@login_required
def property_update(request, pk):
    p = get_object_or_404(Property, pk = pk)

    if p.owner_id != request.user.id: 
        messages.error(request, "You can edit only your own property.");
        return redirect("dashboard")

    f = PropertyForm(request.POST or None, request.FILES or None, instance = p)

    if request.method == "POST" and f.is_valid(): 
        f.save();
        return redirect("dashboard")

    return render(request, "rental/form.html", {
        "form": f,
        "title": "Edit Property"
    })

@login_required
def property_delete(request, pk):
    p = get_object_or_404(Property, pk=pk)

    if p.owner_id!=request.user.id:
        return redirect("dashboard")
    
    if request.method=="POST":
        p.delete()
        return redirect("dashboard")
    
    return render(request,"rental/confirm_delete.html",{"object":p,"type":"property"})

@login_required
def rental_request_create(request, pk):
    p = get_object_or_404(Property, pk = pk)
    if request.user == p.owner or p.availability_status != "available":
        messages.error(request, "You cannot request this property.");
        return redirect("property_detail", pk = pk)

    if RentalRequest.objects.filter(property = p, tenant = request.user, status = "pending").exists():
        messages.error(request, "You already have a pending request.");
        return redirect("property_detail", pk = pk)

    f = RentalRequestForm(request.POST or None)

    if request.method == "POST" and f.is_valid():
        r = f.save(commit = False);
        r.property = p;
        r.tenant = request.user;
        r.save();
        return redirect("dashboard")

    return render(request, "rental/form.html", {
        "form": f,
        "title": "Rental Request"
    })

@login_required 
def owner_request_action(request, pk, action):
    r = get_object_or_404(RentalRequest, pk = pk)
    if r.property.owner_id != request.user.id or r.status != "pending":
        return redirect("dashboard")

    r.status = "accepted" if action == "accept" else "rejected";
    r.save(update_fields = ["status"]);
    return redirect("dashboard")

@login_required
def rental_request_cancel(request, pk):
    r = get_object_or_404(RentalRequest, pk = pk, tenant = request.user)

    if r.status == "pending" and request.method == "POST":
        r.status = "cancelled";
        r.save(update_fields = ["status"]);
        return redirect("dashboard")
    
    return render(request, "rental/confirm_delete.html", {
        "object": r, 
        "type": "request"
    })

@login_required
def review_create(request, pk):
    p = get_object_or_404(Property, pk = pk)

    if not RentalRequest.objects.filter(property = p, tenant = request.user, status = "accepted").exists() or Review.objects.filter(property = p, tenant = request.user).exists():
        messages.error(request, "You are not eligible to review this property.");
        return redirect("property_detail", pk = pk)
    
    f = ReviewForm(request.POST or None)

    if request.method == "POST" and f.is_valid():
        r = f.save(commit = False);
        r.property = p; 
        r.tenant = request.user;
        r.save();
        return redirect("property_detail", pk = pk)
    
    return render(request, "rental/form.html", {
        "form": f,
        "title": "Leave Review"
    })

def search(request):
    q = request.GET.get("q","").strip(); 
    ps = Property.objects.filter(availability_status = "available").select_related("owner")

    if q:ps = ps.filter(Q(title__icontains=q)|Q(description__icontains=q)|Q(location__icontains=q))

    return render(request, "rental/search.html", {
        "properties": ps,
        "query": q
    })
