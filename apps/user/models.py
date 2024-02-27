from django.db import models
from django.utils.translation import gettext_lazy as _
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
        null=True
    )
    class_num = models.CharField(
        max_length=3,
        default='---',
        choices=[
            ('5А', _('5А')),
            ('5Б', _('5Б')),
            ('5В', _('5В')),
            ('5Г', _('5Г')),
            ('5Д', _('5Д')),

            ('6А', _('6А')),
            ('6Б', _('6Б')),
            ('6В', _('6В')),
            ('6Г', _('6Г')),
            ('6Д', _('6Д')),

            ('7А', _('7А')),
            ('7Б', _('7Б')),
            ('7В', _('7В')),
            ('7Г', _('7Г')),
            ('7Д', _('7Д')),

            ('8А', _('8А')),
            ('8Б', _('8Б')),
            ('8В', _('8В')),
            ('8Г', _('8Г')),
            ('8Д', _('8Д')),

            ('9А', _('9А')),
            ('9Б', _('9Б')),
            ('9В', _('9В')),
            ('9Г', _('9Г')),
            ('9Д', _('9Д')),

            ('10А', _('10А')),
            ('10Б', _('10Б')),
            ('10В', _('10В')),
            ('10Г', _('10Г')),
            ('10Д', _('10Д')),

            ('11А', _('11А')),
            ('11Б', _('11Б')),
            ('11В', _('11В')),
            ('11Г', _('11Г')),
            ('11Д', _('11Д')),

            ('-', _('-')),
        ],
        verbose_name=gettext_lazy('Class number'),
        help_text=_('Enter class or a dash (-).')
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

    REQUIRED_FIELDS = ['first_name', 'last_name', 'class_num']

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return  f'{self.first_name} {self.last_name}'


class StudentWork(models.Model):
    image_work = models.ImageField(upload_to='student_works/')
    text_work = models.TextField(blank=True, null=True)
    proven_work = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Student Work {self.id}'

