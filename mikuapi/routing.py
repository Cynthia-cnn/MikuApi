# mikuapi/routing.py

import inspect

from .response import JSONResponse, HTMLResponse
from .request import Request
from .validation import convert_type
from .errors import ValidationError
from .dependencies import Depends
from .docs.openapi import generate_openapi
from .docs.swagger import swagger_ui
from .schema import serialize
from .limiter import limiter
from .logger import logger


class Route:
    def __init__(self, method, path, handler, response_model=None):
        self.method = method
        self.path = path
        self.handler = handler
        self.response_model = response_model
        self.parts = path.strip("/").split("/") if path != "/" else [""]

    def match(self, method, path):
        if self.method != method:
            return None

        path_parts = path.strip("/").split("/") if path != "/" else [""]

        if len(path_parts) != len(self.parts):
            return None

        params = {}

        for p1, p2 in zip(self.parts, path_parts):
            if p1.startswith("{") and p1.endswith("}"):
                params[p1[1:-1]] = p2
            elif p1 != p2:
                return None

        return params


class Router:
    def __init__(self):
        self.routes = []
        self.route_map = {}

        self._add_openapi_route()
        self._add_docs_route()

    def add(self, method, path, handler, response_model=None):
        route = Route(method, path, handler, response_model)
        self.routes.append(route)

        self.route_map[(method, path)] = route

    def get(self, path, response_model=None):
        def decorator(func):
            self.add("GET", path, func, response_model)
            return func
        return decorator

    def post(self, path, response_model=None):
        def decorator(func):
            self.add("POST", path, func, response_model)
            return func
        return decorator

    def _add_openapi_route(self):
        async def openapi_handler(request):
            return JSONResponse(generate_openapi(self.routes))

        self.add("GET", "/openapi.json", openapi_handler)

    def _add_docs_route(self):
        async def docs_handler(request):
            return HTMLResponse(swagger_ui())

        self.add("GET", "/docs", docs_handler)

    async def resolve(self, scope, receive, send):
        request = Request(scope, receive)

        route = self.route_map.get((request.method, request.path))
        params = {}

        if not route:
            for r in self.routes:
                match = r.match(request.method, request.path)
                if match is not None:
                    route = r
                    params = match
                    break

        if not route:
            return JSONResponse({"error": "Not Found"}, 404)

        try:
            logger.info(f"{request.method} {request.path}")

            # RATE LIMIT
            if hasattr(route.handler, "_rate_limit"):
                max_req, window = route.handler._rate_limit
                client = request.scope.get("client", ["unknown"])[0]

                if not limiter.is_allowed(client, max_req, window):
                    return JSONResponse({"error": "Too Many Requests"}, 429)

            kwargs = await self.build_params(route.handler, request, params)

            if inspect.iscoroutinefunction(route.handler):
                result = await route.handler(**kwargs)
            else:
                result = route.handler(**kwargs)

            if route.response_model:
                result = serialize(result, route.response_model)

            if isinstance(result, (JSONResponse, HTMLResponse)):
                return result

            return JSONResponse(result)

        except ValidationError as e:
            return JSONResponse({"error": e.message}, 400)

        except Exception as e:
            logger.error(str(e))
            return JSONResponse({"error": "Internal Server Error"}, 500)

    async def build_params(self, func, request, path_params):
        sig = inspect.signature(func)
        kwargs = {}

        query = request.query_params()

        body = {}
        if request.method == "POST":
            try:
                body = await request.json()
            except:
                body = {}

        for name, param in sig.parameters.items():

            # DEPENDENCY (nested)
            if isinstance(param.default, Depends):
                dep_func = param.default.dependency

                dep_kwargs = await self.build_params(dep_func, request, path_params)

                if inspect.iscoroutinefunction(dep_func):
                    value = await dep_func(**dep_kwargs)
                else:
                    value = dep_func(**dep_kwargs)

                kwargs[name] = value
                continue

            if name == "request":
                kwargs[name] = request
                continue

            value = None

            if name in path_params:
                value = path_params[name]
            elif name in query:
                value = query[name]
            elif name in body:
                value = body[name]

            # DEFAULT SUPPORT
            if value is None:
                if param.default != inspect._empty:
                    kwargs[name] = param.default
                    continue
                raise ValidationError(f"Missing parameter: {name}")

            if param.annotation != inspect._empty:
                value = convert_type(value, param.annotation)

            kwargs[name] = value

        return kwargs