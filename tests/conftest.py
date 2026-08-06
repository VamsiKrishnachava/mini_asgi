import pytest

from mini_asgi.models.request import Request


@pytest.fixture
def default_scope():
    return {
        "method": "GET",
        "path": "/",
        "headers": [],
        "query_string": b"",
    }


@pytest.fixture
def post_scope(default_scope):
    scope = dict(default_scope)
    scope.update({"method": "POST", "path": "/users"})
    return scope


@pytest.fixture
def put_scope(default_scope):
    scope = dict(default_scope)
    scope.update({"method": "PUT", "path": "/users"})
    return scope


@pytest.fixture
def make_http_event():
    def _make(body, more_body=False):
        return {
            "type": "http.request",
            "body": body,
            "more_body": more_body,
        }

    return _make


@pytest.fixture
def request_factory():
    def _build(scope, receive):
        return Request(scope, receive)

    return _build