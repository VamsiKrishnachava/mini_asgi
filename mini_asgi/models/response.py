import json
import html


class Response:
    def __init__(self, body:bytes = b"", status_code:int = 200, 
                 headers: list[tuple[bytes,bytes]] | None = None):
        self.body = body
        self.status_code = status_code
        self.headers = headers

class JSONResponse(Response):
    def __init__(self, body, status_code : int = 200, 
                 headers: list[tuple[bytes,bytes]] | None = None):
        body = json.dumps(body).encode("utf-8")
        headers = ResponseUtils.prepareHeaders(headers, (b"content-type", b"application/json"))
        super().__init(body, status_code, headers)

class PlainTextResponse(Response):
    def __init__(self, body : str, status_code : int = 200,
                 headers: list[tuple[bytes,bytes]] | None = None):
        body = body.encode("utf-8")
        headers = ResponseUtils.prepareHeaders(headers, (b"content-type", b"text/plain"))
        super().__init(body, status_code, headers)

class HTMLResponse(Response):
    def __init__(self, body, status_code: int = 200,
                 headers: list[tuple[bytes,bytes]] | None = None):
        body = str(body).encode("utf-8")
        headers = ResponseUtils.prepareHeaders(headers, (b"content-type", b"text/html"))
        super().__init(body, status_code, headers)

class ResponseUtils:
    @staticmethod
    def prepareHeaders(headers: list[tuple[bytes,bytes]] | None = None, 
                        contentHeader :tuple[bytes,bytes] | None = None ) -> list[tuple[bytes,bytes]]:
        if contentHeader is None:
            return None
        returnHeaders = list(headers or [])
        if not headers is None:
            for header in headers:
                if header[0].lower() == b"content-type":
                    if header[1].lower() == contentHeader.value.lower():
                        return returnHeaders
                    else:
                        raise ValueError("Content type is incorrect in headers.")
        returnHeaders.append(contentHeader)
        return returnHeaders


                    

        



