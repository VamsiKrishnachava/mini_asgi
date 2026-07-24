from mini_asgi.application import MiniASGI
from mini_asgi.models.request import Request

app = MiniASGI()

@app.get("/hello")
def hello():
    return {"message": "Hello, World!"}

@app.post("/json_tester")
async def json_tester(request : Request):
    body = await request.json()
    if request.query_params:
        return {"message" : f"The json is working correctly. The body.age = {body['age']} and params filter = {request.query_params.get('filter', "Did not get any filter")}"}
    return {"message" : f"The json is working correctly. The body.age = {body['age']}"}


@app.get("/")
def root(request : Request):
    return {"message": "Welcome to the app made using MiniASGI framework! the method used is: " + request.method + " and the path is: " + request.path}