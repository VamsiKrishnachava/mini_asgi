import json

from mini_asgi.application import MiniASGI
from mini_asgi.models.request import Request
from mini_asgi.models.response import Response

app = MiniASGI()


def json_response(payload, status_code=200):
    return Response(
        body=json.dumps(payload).encode("utf-8"),
        status_code=status_code,
        headers=[(b"content-type", b"application/json")],
    )


@app.get("/hello")
def hello():
    return json_response({"message": "Hello, World!"})


@app.post("/json_tester")
async def json_tester(request: Request):
    body = await request.json()
    if request.query_params:
        return json_response({
            "message": (
                f"The json is working correctly. The body.age = {body['age']} "
                f"and params filter = {request.query_params.get('filter', 'Did not get any filter')}"
            )
        })
    return json_response({"message": f"The json is working correctly. The body.age = {body['age']}"})


@app.post("/users")
async def postAndReturnUser(request: Request):
    body = await request.json()

    if body.get("userName"):
        return json_response({"userName": body.get("userName")})

    return json_response({"error": "No body sent"}, status_code=400)


@app.get("/")
def root(request: Request):
    return json_response({
        "message": (
            "Welcome to the app made using MiniASGI framework! "
            f"the method used is: {request.method} and the path is: {request.path}"
        )
    })