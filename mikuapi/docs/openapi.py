# mikuapi/docs/openapi.py

import inspect


def generate_openapi(routes):
    paths = {}

    for route in routes:
        path = route.path
        method = route.method.lower()

        sig = inspect.signature(route.handler)

        params = []
        for name, param in sig.parameters.items():
            if name == "request":
                continue

            params.append({
                "name": name,
                "in": "query",
                "required": True,
                "schema": {"type": "string"}
            })

        paths.setdefault(path, {})
        paths[path][method] = {
            "summary": route.handler.__name__,
            "parameters": params,
            "responses": {
                "200": {"description": "Success"}
            }
        }

    return {
        "openapi": "3.0.0",
        "info": {"title": "MikuAPI", "version": "1.0"},
        "paths": paths
    }