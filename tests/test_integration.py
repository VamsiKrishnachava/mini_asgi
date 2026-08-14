import pytest

from mini_asgi.application import MiniASGI
from mini_asgi.models.response import JSONResponse, PlainTextResponse
from mini_asgi.router import ApiRouter


@pytest.mark.asyncio
async def test_app_returns_404_for_unknown_route():
    app = MiniASGI()
    sent = []

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        sent.append(message)

    scope = {"type": "http", "method": "GET", "path": "/missing", "headers": [], "query_string": b""}

    await app(scope, receive, send)

    assert sent[0]["type"] == "http.response.start"
    assert sent[0]["status"] == 404
    assert sent[1]["body"] == b"Route not found"


@pytest.mark.asyncio
async def test_app_executes_route_and_returns_response():
    app = MiniASGI()
    sent = []

    @app.get("/hello")
    async def hello(request):
        return JSONResponse({"message": "hi"})

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        sent.append(message)

    scope = {"type": "http", "method": "GET", "path": "/hello", "headers": [], "query_string": b""}

    await app(scope, receive, send)

    assert sent[0]["type"] == "http.response.start"
    assert sent[0]["status"] == 200
    assert sent[0]["headers"] == [(b"content-type", b"application/json")]
    assert sent[1]["body"] == b'{"message": "hi"}'


@pytest.mark.asyncio
async def test_app_supports_path_parameters():
    app = MiniASGI()
    sent = []

    @app.get("/users/{user_id}")
    async def read_user(user_id, request):
        return PlainTextResponse(user_id)

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        sent.append(message)

    scope = {"type": "http", "method": "GET", "path": "/users/42", "headers": [], "query_string": b""}

    await app(scope, receive, send)

    assert sent[1]["body"] == b"42"


@pytest.mark.asyncio
async def test_include_router_registers_routes():
    app = MiniASGI()
    router = ApiRouter(prefix="/api")

    @router.get("/users")
    async def list_users(request):
        return JSONResponse({"count": 1})

    app.include_router(router)

    sent = []

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        sent.append(message)

    scope = {"type": "http", "method": "GET", "path": "/api/users", "headers": [], "query_string": b""}

    await app(scope, receive, send)

    assert sent[0]["status"] == 200
    assert sent[1]["body"] == b'{"count": 1}'


@pytest.mark.asyncio
async def test_app_rejects_non_response_return_values():
    app = MiniASGI()

    @app.get("/bad")
    async def bad_route(request):
        return {"message": "wrong"}

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        return None

    scope = {"type": "http", "method": "GET", "path": "/bad", "headers": [], "query_string": b""}

    with pytest.raises(TypeError):
        await app(scope, receive, send)
