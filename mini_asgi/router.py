class ApiRouter:
    def __init__(self, prefix: str = "", tags: list[str] = None):
        self.prefix = prefix
        self.tags = tags or []
        self.routes = {}

    def get(self, path: str):
        def decorator(func):
            full_path = self.prefix + path
            self.routes[("GET", full_path)] = func
            return func
        return decorator 
    
    def post(self, path: str):
        def decorator(func):
            full_path = self.prefix + path
            self.routes[("POST", full_path)] = func
            return func
        return decorator
    
    def put(self, path: str):
        def decorator(func):
            full_path = self.prefix + path
            self.routes[("PUT", full_path)] = func
            return func
        return decorator
    
    def delete(self, path: str):
        def decorator(func):
            full_path = self.prefix + path
            self.routes[("DELETE", full_path)] = func
            return func
        return decorator
    
    def patch(self, path: str):
        def decorator(func):
            full_path = self.prefix + path
            self.routes[("PATCH", full_path)] = func
            return func
        return decorator