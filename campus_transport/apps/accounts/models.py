from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        DRIVER = "driver", "Driver"
        TRANSPORT_ADMIN = "transport_admin", "Transport Admin"
        SUPER_ADMIN = "super_admin", "Super Admin"

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=32, choices=Role.choices)
    student_id = models.CharField(max_length=32, blank=True)
    employee_id = models.CharField(max_length=32, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.email})"

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name.split(" ")[0]

    @property
    def username(self):
        return self.email

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def is_driver(self):
        return self.role == self.Role.DRIVER

    @property
    def is_transport_admin(self):
        return self.role == self.Role.TRANSPORT_ADMIN

    @property
    def is_super_admin(self):
        return self.role == self.Role.SUPER_ADMIN
