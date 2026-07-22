class Request:
        def __init__(self, scope):
            self.scope = scope
            self.method = scope['method']
            self.path = scope['path']
            self.headers = dict(scope['headers'])
            self.query_string = scope['query_string']