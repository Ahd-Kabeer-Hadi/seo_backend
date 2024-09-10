from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User, YouTubeAccount

class YouTubeAccountInline(admin.TabularInline):
    model = YouTubeAccount
    extra = 1

class UserAdmin(DefaultUserAdmin):
    inlines = [YouTubeAccountInline]

    # Customize the fields to match your User model
    list_display = ('email', 'first_name', 'username', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'username', 'about')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'start_date')}),
    )

admin.site.register(User, UserAdmin)
