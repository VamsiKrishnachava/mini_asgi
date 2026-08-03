import json

from mini_asgi.models.response import Response
from mini_asgi.router import ApiRouter
from mini_asgi.models.request import Request
from mini_asgi.models.route import Route

class MiniASGI:
    def __init__(self):
        self.routes = {}

    def get(self, path):
        def decorator(func):
            self._registerRoute(Route("GET", path, func))
            return func
        return decorator

    def post(self, path):
        def decorator(func):
            self._registerRoute(Route("POST", path, func)) 
            return func
        return decorator
    
    def put(self, path):
        def decorator(func):
            self._registerRoute(Route("PUT", path, func)) 
            return func
        return decorator
    
    def delete(self, path):
        def decorator(func):
            self._registerRoute(Route("DELETE", path, func)) 
            return func
        return decorator
    
    def patch(self, path):
        def decorator(func):
            self._registerRoute(Route("PATCH", path, func)) 
            return func
        return decorator
    
    def include_router(self, router : ApiRouter):
        for (method, path), func in router.routes.items():
            if (method, path) in self.routes:
                raise ValueError(f"Route {method} {path} already exists in the main app.")
            self.routes[(method, path)] = func

    async def __call__(self, scope, receive, send):
        path = scope['path']
        method = scope['method'].upper()
        route = self.routes.get((method, path))
        if not route:
            route = self._find_route(method, path)

        if not route:
            await self._send_header_helper(404, [(b'content-type', b'text/plain')], send)
            await self._send_body_helper(b"Route not found", send)
            return

        response = await self._call_function(scope, receive, route)

        if not  isinstance(response,Response):
            raise TypeError("The response is not of type Response.")

        await self._send_header_helper(response.status_code, response.headers, send)
        await self._send_body_helper(response.body, send)



# --------------- Helper methods ---------------
    def _registerRoute(self, route:Route):
            """
                This fucntion helps in registering a route in the app. 
            """    
            self.routes[(route.method, route.path)] = route
            return

    async def _call_function(self, scope, receive, route = None):

        function = route.func
        requestParameter = route.expectedRequestParameter
        expectedRequestParameter = requestParameter.name if requestParameter else None
        
        # Instead of having multiple for different cases, 
        # we can build the arguments. 
        # This way we will only have 2 path ways async and sync. 
        kwargs = {}
        if expectedRequestParameter:
            kwargs[expectedRequestParameter] = Request(scope, receive)

        for name, value in (route.match_path(scope['path']) or {}).items():
            kwargs[name] = value

        if route.isAsync:
            return await function(**kwargs)
        else: 
            return function(**kwargs)
               
    def _find_route(self, method, path):
        for (route_method, route_path), route in self.routes.items():
            if route_method != method:
                continue
            if route.match_path(path) is not None:
                return route
        return None

    async def _send_header_helper(self, status, headers, send):
        """
        Helper method to send HTTP response headers.
        """
        await send({
            'type': 'http.response.start',
            'status': status,
            'headers': headers,
        })

    async def _send_body_helper(self, body, send, more_body=False):
        """
        Helper method to send HTTP response body.
        """
        await send({
            'type': 'http.response.body',
            'body': body,
            'more_body': False,
        })