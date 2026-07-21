from mini_asgi.application import MiniASGI

app = MiniASGI()

@app.get("/hello")
def hello():
    return {"message": "Hello, World!"}

@app.get("/")
async def root():
    return {"message": "Welcome to the app made using MiniASGI framework!"}