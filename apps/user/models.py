from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)

from django.utils.translation import gettext_lazy

from apps.user.manager import UserManager


class SchoolClass(models.Model):
    name_class = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'SchoolClass'
        verbose_name_plural = 'SchoolClasses'

    def __str__(self):
        return f'{self.name_class}'


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
    student_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    username = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    phone = models.CharField(
        max_length=75,
        null=True
    )
    is_superuser = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
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
        return f'{self.first_name} {self.last_name}'
