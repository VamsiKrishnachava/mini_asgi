import pytest

from mini_asgi.application import MiniASGI
from mini_asgi.models.request import Request
from mini_asgi.models.response import (
    HTMLResponse,
    JSONResponse,
    PlainTextResponse,
    Response,
    ResponseUtils,
)
from mini_asgi.router import ApiRouter


def test_response_stores_body_status_and_headers():
    response = Response(body=b"ok", status_code=201, headers=[(b"x-test", b"1")])

    assert response.body == b"ok"
    assert response.status_code == 201
    assert response.headers == [(b"x-test", b"1")]


def test_json_response_serializes_body_and_sets_content_type():
    response = JSONResponse({"name": "John"})

    assert response.body == b'{"name": "John"}'
    assert response.status_code == 200
    assert response.headers == [(b"content-type", b"application/json")]


def test_plain_text_response_encodes_body_and_sets_content_type():
    response = PlainTextResponse("hello")

    assert response.body == b"hello"
    assert response.headers == [(b"content-type", b"text/plain")]


def test_html_response_converts_body_to_bytes_and_sets_content_type():
    response = HTMLResponse("<h1>Hi</h1>")

    assert response.body == b"<h1>Hi</h1>"
    assert response.headers == [(b"content-type", b"text/html")]


def test_response_utils_preserves_existing_content_type():
    headers = [(b"content-type", b"application/json")]

    prepared = ResponseUtils.prepareHeaders(headers, (b"content-type", b"application/json"))

    assert prepared == headers


def test_response_utils_adds_content_type_when_missing():
    prepared = ResponseUtils.prepareHeaders(None, (b"content-type", b"text/plain"))

    assert prepared == [(b"content-type", b"text/plain")]


def test_response_utils_raises_for_mismatched_content_type():
    headers = [(b"content-type", b"text/plain")]

    with pytest.raises(ValueError):
        ResponseUtils.prepareHeaders(headers, (b"content-type", b"application/json"))
