from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def user_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        user = request.user
        if user.role == "USER" and not user.is_superuser:
            return view_func(request, *args, **kwargs)
        # admins/superusers hitting user area -> admin dashboard (A1)
        if user.role == "ADMIN" or user.is_superuser:
            return redirect("accounts:admin_dashboard")
        messages.error(request, "You do not have permission to view that page.")
        return redirect("accounts:post_login")

    return _wrapped


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        user = request.user
        if user.role == "ADMIN" or user.is_superuser:  # A1
            return view_func(request, *args, **kwargs)
        messages.error(request, "You do not have permission to view that page.")
        return redirect("accounts:post_login")

    return _wrapped
