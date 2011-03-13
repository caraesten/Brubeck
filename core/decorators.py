# Imports from Django
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def is_editor(user):
    """
    Checks whether or not a person is an editor, based on that person's 
    membership in the "Editorial Board" group.
    """
    if user.is_superuser:
        return True
    for group in user.groups.all():
        if group.name == 'Editorial Board':
            return True
            break
    return False

def staff_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    actual_decorator = user_passes_test(lambda u: u.is_staff or u.is_superuser, redirect_field_name=redirect_field_name)
    if function:
        return actual_decorator(function)
    return actual_decorator

def editor_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    actual_decorator = user_passes_test(lambda u: is_editor(u), redirect_field_name=redirect_field_name)
    if function:
        return actual_decorator(function)
    return actual_decorator
