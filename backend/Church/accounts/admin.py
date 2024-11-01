from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'firstname', 'lastname', 'email', 'role', 'is_staff')  # Customize fields shown in the admin list view
    search_fields = ('username', 'email', 'firstname', 'lastname')  # Enable search functionality
    list_filter = ('role', 'is_staff', 'is_active')  # Add filters for easier management
