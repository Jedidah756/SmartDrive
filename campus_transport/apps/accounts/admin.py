from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "role", "student_id", "employee_id", "is_staff")
    ordering = ("email",)
    search_fields = ("email", "name", "student_id", "employee_id")
    list_filter = ("role", "is_active", "is_staff")
