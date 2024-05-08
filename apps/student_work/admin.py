from django.contrib import admin
from apps.student_work.models import (
    StudentWork,
    Example,
    TypeStudentWork
)


@admin.register(TypeStudentWork)
class TypeStudentWorkAdmin(admin.ModelAdmin):
    list_display = [
        'type_work',
        'name_work',
        'writing_date',
        'example',
        'school_class',
        'teacher',
    ]
    list_filter = ['type_work', 'name_work', 'writing_date', 'school_class', 'teacher']
    search_fields = ['type_work', 'name_work', 'teacher']


@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    list_display = [
        'name_work',
        'image_work',
        'text_work',
    ]
    list_filter = ['name_work']
    search_fields = ['name_work']


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


