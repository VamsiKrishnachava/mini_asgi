from mini_asgi.models.request import Request

import pytest

@pytest.mark.asyncio
async def test_request_body():
    async def receive():
        return {
            "type": "http.request",
            "body": b'{"name": "John"}',
            "more_body": False,
        }

    scope = {
        "method": "POST",
        "path": "/users",
        "headers": [],
        "query_string": b"",
    }

    request = Request(scope, receive)
    body = await request.body()
    assert body == b'{"name": "John"}'