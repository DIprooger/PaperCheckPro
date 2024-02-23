from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)

from django.utils.translation import gettext_lazy

from apps.user.manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=120,
        unique=True,
        verbose_name=gettext_lazy('Email address')
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name=gettext_lazy('First name')
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name=gettext_lazy('Last name')
    )
    username = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    phone = models.CharField(
        max_length=75,
        blank=True,
        null=True
    )
    is_superuser = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    date_delete = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


class SubjectGrade(models.Model):
    subject = models.CharField(max_length=100)
    date = models.DateField()
    work_type = models.CharField(max_length=100)
    grade = models.IntegerField()
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)

    def __str__(self):
        return self.subject


class Album(models.Model):
    name = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name