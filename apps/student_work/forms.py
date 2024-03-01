from django import forms
from .models import Example, StudentWork


class ExampleForm(forms.ModelForm):
    class Meta:
        model = Example
        fields = ['name_work', 'image_work']


class StudentWorkForm(forms.ModelForm):
    class Meta:
        model = StudentWork
        fields = ['name_work', 'writing_date', 'number_of_tasks', 'image_work', 'example', 'student', 'teacher']