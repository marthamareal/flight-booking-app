"""Methods used for validation"""

from rest_framework import serializers
import re


def validate_field(field, pattern, error_message):
    """Validates an id_number
    Args:
        field (str): field to validate
        pattern (str): regex pattern to match th the field
        error_message (str): error message to be raised
    Raises:
        ValidationError: if provided field does not match the pattern
    Returns:
        field (str): validated field
    """
    if not re.fullmatch(pattern, field):
        raise serializers.ValidationError(error_message)
    return field
