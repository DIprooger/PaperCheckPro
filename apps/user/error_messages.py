EMAIL_REQUIRED_MESSAGE = 'Email is required'
FIRST_NAME_REQUIRED_MESSAGE = 'First name is required'
LAST_NAME_REQUIRED_MESSAGE = 'Last name is required'
NOT_IS_STAFF_ERROR = 'Admin must be is staff'
NOT_IS_SUPERUSER_ERROR = 'Admin must be a superuser'
PASSWORDS_DO_NOT_MATCH_ERROR = 'Passwords do not matches. Please, try again'
ROLE_REQUIRED_MESSAGE = 'Role is required'


def UNVALID_EMAIL_ERROR(message):
    return f'{message}.\n Please, enter a valid email'
