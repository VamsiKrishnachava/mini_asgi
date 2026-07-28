class Response:

    def __init__(self, body:bytes = b"", status_code:int = 200, 
                 headers: list[tuple[bytes,bytes]] | None = None):
        self.body = body
        self.status_code = status_code
        self.headers = headers