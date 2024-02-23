from django.contrib import admin
from apps.user.models import User, SubjectGrade, Album


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



@admin.register(SubjectGrade)
class SubjectGradeAdmin(admin.ModelAdmin):
    list_display = ('subject', 'date', 'work_type', 'grade', 'photo')
    search_fields = ('subject', 'work_type')
    list_filter = ('date',)

admin.site.register(Album)
