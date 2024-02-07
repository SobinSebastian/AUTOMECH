from django.shortcuts import redirect
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import User
def manager_required(view_func):
    @wraps(view_func)
    @login_required(login_url='/account/login/')  # Use your login URL
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == User.Role.MANAGER:
            return view_func(request, *args, **kwargs)
        else:
            if request.user.is_authenticated:
                next_url = request.get_full_path()
            else:
                next_url = request.build_absolute_uri()
            return redirect('/account/login/', next=next_url)
    return _wrapped_view