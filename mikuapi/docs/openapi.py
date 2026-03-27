import inspect
from ..schema import is_model


def python_type_to_openapi(t):
    if t == int:
        return {"type": "integer"}
    if t == float:
        return {"type": "number"}
    if t == bool:
        return {"type": "boolean"}
    if t == list:
        return {"type": "array", "items": {"type": "string"}}
    return {"type": "string"}


def model_to_schema(model):
    return {
        "type": "object",
        "properties": {
            field: python_type_to_openapi(ftype)
            for field, ftype in model.__annotations__.items()
        },
        "required": list(model.__annotations__.keys())
    }


def generate_openapi(routes):
    paths = {}
    components = {"schemas": {}}

    for route in routes:
        path = route.path
        method = route.method.lower()

        sig = inspect.signature(route.handler)

        parameters = []
        request_body = None
        response_schema = None

        for name, param in sig.parameters.items():

            if name == "request":
                continue

            annotation = param.annotation

            # PATH PARAM
            if "{" + name + "}" in path:
                parameters.append({
                    "name": name,
                    "in": "path",
                    "required": True,
                    "schema": python_type_to_openapi(annotation)
                })

            # BODY (MODEL)
            elif is_model(annotation):
                schema_name = annotation.__name__

                components["schemas"][schema_name] = model_to_schema(annotation)

                request_body = {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": f"#/components/schemas/{schema_name}"
                            }
                        }
                    }
                }

            # QUERY
            else:
                parameters.append({
                    "name": name,
                    "in": "query",
                    "required": param.default == inspect._empty,
                    "schema": python_type_to_openapi(annotation)
                })

        # RESPONSE MODEL
        if route.response_model and is_model(route.response_model):
            schema_name = route.response_model.__name__

            components["schemas"][schema_name] = model_to_schema(route.response_model)

            response_schema = {
                "$ref": f"#/components/schemas/{schema_name}"
            }

        else:
            response_schema = {"type": "object"}

        paths.setdefault(path, {})
        paths[path][method] = {
            "summary": route.handler.__name__,
            "parameters": parameters,
            "responses": {
                "200": {
                    "description": "Success",
                    "content": {
                        "application/json": {
                            "schema": response_schema
                        }
                    }
                }
            }
        }

        if request_body:
            paths[path][method]["requestBody"] = request_body

    return {
        "openapi": "3.0.0",
        "info": {
            "title": "MikuAPI",
            "version": "1.0.0"
        },
        "paths": paths,
        "components": components
    }