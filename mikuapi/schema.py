import inspect
from .errors import ValidationError
from .validation import convert_type


class BaseModel:
    def __init__(self, **data):
        annotations = getattr(self, "__annotations__", {})

        for field, field_type in annotations.items():

            if field in data:
                value = data[field]
            elif hasattr(self, field):
                value = getattr(self, field)  # default value
            else:
                raise ValidationError(f"Missing field: {field}")

            try:
                value = self._convert(value, field_type)
            except:
                raise ValidationError(f"Invalid type for field: {field}")

            setattr(self, field, value)

    def _convert(self, value, field_type):
        if getattr(field_type, "__origin__", None) == list:
            inner = field_type.__args__[0]
            return [convert_type(v, inner) for v in value]

        return convert_type(value, field_type)

    def dict(self):
        return {
            field: getattr(self, field)
            for field in self.__annotations__
        }


def is_model(annotation):
    return inspect.isclass(annotation) and issubclass(annotation, BaseModel)


def serialize(data, model):
    if is_model(model):

        if isinstance(data, model):
            return data.dict()

        if isinstance(data, dict):
            obj = model(**data)
            return obj.dict()

    return data