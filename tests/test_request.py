import json

import pytest


def test_request_initializes_basic_fields(post_scope, request_factory):
    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    request = request_factory(post_scope, receive)

    assert request.method == "POST"
    assert request.path == "/users"
    assert request.headers == {}
    assert request.query_params == {}
    assert request.cookie == {}


def test_request_parses_headers_query_params_and_cookies(default_scope, request_factory):
    scope = dict(default_scope)
    scope.update(
        {
            "method": "GET",
            "path": "/search",
            "headers": [
                (b"content-type", b"application/json"),
                (b"x-test", b"abc"),
                (b"cookie", b"session=123; theme=dark"),
            ],
            "query_string": b"page=2&filter=active",
        }
    )

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    request = request_factory(scope, receive)

    assert request.headers["content-type"] == "application/json"
    assert request.headers["x-test"] == "abc"
    assert request.query_params == {"page": ["2"], "filter": ["active"]}
    assert request.cookie == {"session": "123", "theme": "dark"}


def test_request_ignores_malformed_cookie_entries(default_scope, request_factory):
    scope = dict(default_scope)
    scope.update(
        {
            "headers": [(b"cookie", b"valid=1; broken; another=2")],
            "query_string": b"",
        }
    )

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    request = request_factory(scope, receive)

    assert request.cookie == {"valid": "1", "another": "2"}


@pytest.mark.asyncio
async def test_request_body(post_scope, request_factory, make_http_event):
    async def receive():
        return make_http_event(b'{"name": "John"}')

    request = request_factory(post_scope, receive)
    body = await request.body()
    assert body == b'{"name": "John"}'


@pytest.mark.asyncio
async def test_empty_request_body(put_scope, request_factory, make_http_event):
    async def receive():
        return make_http_event(b"")

    request = request_factory(put_scope, receive)
    body = await request.body()
    assert body == b""


@pytest.mark.asyncio
async def test_request_body_cache(post_scope, request_factory, make_http_event):
    calls = 0

    async def receive():
        nonlocal calls
        calls += 1
        return make_http_event(b'{"name": "John"}')

    request = request_factory(post_scope, receive)
    body = await request.body()
    assert body == b'{"name": "John"}'
    body = await request.body()
    assert calls == 1


@pytest.mark.asyncio
async def test_request_body_streaming(post_scope, request_factory, make_http_event):
    events = iter(
        [
            make_http_event(b'{"name": ', more_body=True),
            make_http_event(b'"John', more_body=True),
            make_http_event(b' grishim"}', more_body=False),
        ]
    )

    async def receive():
        nonlocal events
        return next(events)

    request = request_factory(post_scope, receive)
    body = await request.body()
    assert body == b'{"name": "John grishim"}'


@pytest.mark.asyncio
async def test_request_valid_json(post_scope, request_factory, make_http_event):
    async def receive():
        return make_http_event(b'{"name": "John"}')

    request = request_factory(post_scope, receive)
    data = await request.json()
    assert data == {"name": "John"}


@pytest.mark.asyncio
async def test_request_empty_json(post_scope, request_factory, make_http_event):
    async def receive():
        return make_http_event(b"")

    request = request_factory(post_scope, receive)
    data = await request.json()
    assert data is None


@pytest.mark.asyncio
async def test_request_invalid_json(post_scope, request_factory, make_http_event):
    async def receive():
        return make_http_event(b'{"name": "John"')

    request = request_factory(post_scope, receive)
    with pytest.raises(json.JSONDecodeError):
        await request.json()


@pytest.mark.asyncio
async def test_request_json_cache(post_scope, request_factory, make_http_event):
    calls = 0

    async def receive():
        nonlocal calls
        calls += 1
        return make_http_event(b'{"name": "John"}')

    request = request_factory(post_scope, receive)
    data = await request.json()
    assert data == {"name": "John"}
    data = await request.json()
    assert calls == 1
