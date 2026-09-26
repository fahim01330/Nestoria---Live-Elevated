from django.contrib import messages
from django.shortcuts import redirect

class RoleRequiredMiddleware:
    def __init__(self, get_response): 
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            role = getattr(getattr(request.user, "profile", None), "role", None)

            if request.path.startswith("/owner/") and role != "owner": 
                messages.error(request, "Only property owners can access this area.");
                return redirect("dashboard")
            
            if request.path.startswith("/tenant/") and role != "tenant": 
                messages.error(request, "Only tenants can access this area.");
                return redirect("dashboard")
        
        return self.get_response(request)
