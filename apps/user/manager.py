from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from django.utils.translation import gettext_lazy

from apps.user.error_messages import (
    UNVALID_EMAIL_ERROR,
    EMAIL_REQUIRED_MESSAGE,
    LAST_NAME_REQUIRED_MESSAGE,
    FIRST_NAME_REQUIRED_MESSAGE,
    NOT_IS_STAFF_ERROR,
)


class UserManager(BaseUserManager):

    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError as err:
            raise ValueError(
                gettext_lazy(UNVALID_EMAIL_ERROR(err.message))
            )

    def create_user(self, email, first_name, last_name, password, **extra_fields):
        if email:
            email = self.normalize_email(email=email)
            self.email_validator(email=email)
        else:
            raise ValueError(
                gettext_lazy(EMAIL_REQUIRED_MESSAGE)
            )

        if not first_name:
            raise ValueError(
                gettext_lazy(FIRST_NAME_REQUIRED_MESSAGE)
            )

        if not last_name:
            raise ValueError(
                gettext_lazy(LAST_NAME_REQUIRED_MESSAGE)
            )

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **extra_fields
        )

        user.save(using=self._db)

        user.set_password(password)

        return user

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        if not extra_fields.get('is_staff'):
            raise ValueError(
                gettext_lazy(NOT_IS_STAFF_ERROR)
            )

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_moderator(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_moderator', True)
        extra_fields.setdefault('is_verified', True)

        if not extra_fields.get('is_staff'):
            raise ValueError(
                gettext_lazy(NOT_IS_STAFF_ERROR)
            )

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user
