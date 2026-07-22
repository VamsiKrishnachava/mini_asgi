from mini_asgi.application import MiniASGI
from mini_asgi.models.request import Request

app = MiniASGI()

@app.get("/hello")
def hello():
    return {"message": "Hello, World!"}

@app.get("/")
def root(request : Request, no:Request):
    return {"message": "Welcome to the app made using MiniASGI framework! the method used is: " + request.method + " and the path is: " + request.path}