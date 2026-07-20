import inspect

class MiniASGI:
    def __init__(self):
        self.routes = {}

    def get(self, path):
        def decorator(func):
            self.routes[("GET", path)] = func
            return func
        return decorator

    def post(self, path):
        def decorator(func):
            self.routes[("POST", path)] = func
            return func
        return decorator

    async def __call__(self, scope, receive, send):
        path = scope['path']
        method = scope['method'].upper()
        function = self.routes.get((method, path))
        if function:
            if inspect.iscoroutinefunction(function):
                result = await function()
            else:
                result = function()
        else:
            raise Exception("Route not found")