from fastapi import FastAPI

from users import urls
app = FastAPI()

app.include_router(urls.router, prefix="/users")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

