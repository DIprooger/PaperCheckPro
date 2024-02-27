from django.db import models
from apps.user.models import User


class Example(models.Model):
    image_work = models.ImageField(upload_to='example')
    text_work = models.TextField(null=True)


class StudentWork(models.Model):
    name_work = models.CharField(max_length=55)
    writing_date = models.DateTimeField()
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
    text_work = models.TextField(null=True)
    proven_work = models.TextField(null=True)
    assessment = models.CharField(max_length=10, null=True)
    teacher = models.ForeignKey(
        User,
        related_name='teacher',
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name_work
