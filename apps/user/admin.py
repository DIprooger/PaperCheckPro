from django.contrib import admin
from apps.user.models import User, SchoolClass


@admin.register(SchoolClass)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name_class']
    list_filter = ['name_class']
    search_fields = ['name_class']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_superuser',
        'is_moderator',
        'date_joined',
        'last_login',
        'date_delete'
    ]
    list_filter = ['email', 'is_active', 'date_joined', 'last_login']
    search_fields = ['email', 'first_name', 'last_name']


