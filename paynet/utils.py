"""
the payment app utilities
"""
from django.conf import settings


# pylint: disable=all
def get_admin_model(name):
    """
    Check if the given name is a custom admin.

    Args:
        name (str): The name to check.

    Returns:
        bool: True if the name is a custom admin, False otherwise.
    """
    if name in settings.INSTALLED_APPS:
        from unfold.admin import ModelAdmin
        return ModelAdmin

    from django.contrib.admin import ModelAdmin
    return ModelAdmin
