# mikuapi/schema.py

import inspect


class BaseModel:
    def dict(self):
        return {
            k: getattr(self, k)
            for k in self.__annotations__
        }


def serialize(data, model):
    if isinstance(data, dict):
        result = {}

        for field, field_type in model.__annotations__.items():
            if field in data:
                try:
                    result[field] = field_type(data[field])
                except:
                    raise ValueError(f"Invalid type for field '{field}'")

        return result

    return data