from django.db import models
from apps.user.models import User, SchoolClass


class Example(models.Model):
    name_work = models.TextField(max_length=55)
    image_work = models.ImageField(upload_to='example')
    text_work = models.TextField(null=True)

    def __str__(self):
        return self.name_work


class TypeStudentWork(models.Model):
    type_work = models.CharField(max_length=55)
    name_work = models.CharField(max_length=55)
    writing_date = models.DateTimeField()
    example = models.ForeignKey(
        Example,
        on_delete=models.SET_NULL,
        null=True
    )
    school_class = models.ForeignKey(
        SchoolClass,
        related_name='school_class',
        on_delete=models.SET_NULL,
        null=True
    )
    teacher = models.ForeignKey(
        User,
        related_name='teacher_trainer',
        on_delete=models.SET_NULL,
        null=True
    )


class StudentWork(models.Model):
    name_work = models.CharField(max_length=55)
    writing_date = models.DateTimeField()
    student_type = models.ForeignKey(
        TypeStudentWork,
        related_name='type_works',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    number_of_tasks = models.CharField(max_length=5, default="5")
    student = models.ForeignKey(
        User,
        related_name='student',
        on_delete=models.SET_NULL,
        null=True
    )
    example = models.ForeignKey(
        Example,
        on_delete=models.SET_NULL,
        null=True
    )
    image_work = models.ImageField(upload_to='image')
    text_work = models.TextField(null=True, blank=True)
    proven_work = models.TextField(null=True, blank=True)
    assessment = models.CharField(max_length=10, null=True, blank=True)
    teacher = models.ForeignKey(
        User,
        related_name='teacher',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name_work
