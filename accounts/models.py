from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """Custom manager for email-based User (no username field)."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address.")
        if not password:
            raise ValueError("A password is required.")  # BR-03
        email = self.normalize_email(email)
        extra_fields.setdefault("role", User.Roles.USER)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # A1: create_superuser sets role='ADMIN', is_staff=True, is_superuser=True
        extra_fields["role"] = User.Roles.ADMIN
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Roles(models.TextChoices):
        USER = "USER", "User"
        ADMIN = "ADMIN", "Admin"

    email = models.EmailField(unique=True)  # BR-01
    full_name = models.CharField(max_length=150)
    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.USER)  # BR-02
    contact_number = models.CharField(max_length=30, blank=True)
    profile_photo = models.ImageField(upload_to="profiles/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    def save(self, *args, **kwargs):
        # A1: force role='ADMIN' if is_superuser or is_staff is True
        if self.is_superuser or self.is_staff:
            self.role = self.Roles.ADMIN
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
