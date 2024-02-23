from django.contrib import admin
from apps.student_work.models import StudentWork


@admin.register(StudentWork)
class StudentWorkAdmin(admin.ModelAdmin):
    list_display = [
        'name_work',
        'writing_date',
        'student',
        'image_work',
        'text_work',
        'proven_work',
        'assessment',
        'teacher',
        'created_at',
        'updated_at',
        'deleted_at'
    ]
    list_filter = ['name_work', 'writing_date', 'student', 'teacher']
    search_fields = ['name_work', 'writing_date', 'student']

