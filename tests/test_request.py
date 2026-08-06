import json

import pytest


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
        return make_http_event(b'')

    request = request_factory(put_scope, receive)
    body = await request.body()
    assert body == b''


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
    events = iter([
        make_http_event(b'{"name": ', more_body=True),
        make_http_event(b'"John', more_body=True),
        make_http_event(b' grishim"}', more_body=False),
    ])

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
        return make_http_event(b'')

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