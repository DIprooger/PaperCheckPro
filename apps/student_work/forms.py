from django import forms
from .models import (
    Example,
    StudentWork,
    TypeStudentWork
)


class ExampleForm(forms.ModelForm):
    class Meta:
        model = Example
        fields = ['name_work', 'image_work']


class TypeStudentWorkForm(forms.ModelForm):
    class Meta:
        model = TypeStudentWork
        fields = [
            'type_work',
            'name_work',
            'writing_date',
            'example',
            'school_class',
            'teacher'
        ]


class StudentWorkForm(forms.ModelForm):
    class Meta:
        model = StudentWork
        fields = [
            'name_work',
            'writing_date',
            'student_type',
            'number_of_tasks',
            'student',
            'image_work',
            'example',
            'teacher'
        ]
