import json

class Request:
        def __init__(self, scope, receive):
            self.scope = scope
            self.method = scope['method']
            self.path = scope['path']
            self.headers = dict(scope['headers'])
            self.query_string = scope['query_string']
            self._receive = receive
            self._body = None
            self._json = None
                 

        async def body(self) -> bytes:
            if self._body is not None:
                 return self._body
            self._body = b''
            while True:
                event = await self._receive()
                self._body+=event.get("body", b'')
                if not event.get("more_body", False):
                     break
            return self._body

        async def json(self):
             if self._json is not None:
                  return self._json
             
             body = await self.body()
             if body == b"":
                return None
             self._json = json.loads(body)
             return self._json
