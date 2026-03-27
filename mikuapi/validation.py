

from .errors import ValidationError


def convert_type(value, to_type):
    try:
        return to_type(value)
    except:
        raise ValidationError(f"Invalid type for value '{value}', expected {to_type.__name__}")