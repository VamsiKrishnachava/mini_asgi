import inspect
import json

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

            # Convert the result to JSON and send the response. We assume the result is a dictionary.
            if not isinstance(result, dict):
                result = {"result": result}
            response_body = json.dumps(result).encode('utf-8')
            await self._send_header_helper(200, [(b'content-type', b'application/json')], send)
            await self._send_body_helper(response_body, send)
        else:
            await self._send_header_helper(404, [(b'content-type', b'text/plain')], send)
            await self._send_body_helper(b"Route not found", send)


# --------------- Helper methods to send headers and body ---------------
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