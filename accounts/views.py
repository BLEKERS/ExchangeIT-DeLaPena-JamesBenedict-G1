from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .decorators import admin_required, user_required
from .forms import LoginForm, ProfileEditForm, RegisterForm

User = get_user_model()


def home_redirect(request):
    if request.user.is_authenticated:
        return redirect("accounts:post_login")
    return redirect("accounts:login")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect("accounts:post_login")
        messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:post_login")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            email = User.objects.filter(email__iexact=email).values_list("email", flat=True).first() or email
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully.")
                return redirect("accounts:post_login")
            messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Please enter a valid email and password.")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("accounts:login")


@login_required
def post_login(request):
    user = request.user
    if user.role == "ADMIN" or user.is_superuser:
        return redirect("accounts:admin_dashboard")
    return redirect("accounts:user_dashboard")


@login_required
@user_required
def user_dashboard(request):
    return render(request, "dashboards/user_dashboard.html")


@login_required
@admin_required
def admin_dashboard(request):
    return render(request, "dashboards/admin_dashboard.html")


@login_required
def profile_view(request):
    return render(request, "accounts/profile.html", {"profile_user": request.user})


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:profile")
        messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, "accounts/profile_edit.html", {"form": form})
