from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from users import urls
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

jinja2 = Jinja2Templates(directory="templates")

app.include_router(urls.router, prefix="/users")


def remove_subdomain(value: str):
    return value.split('.')[-1]

jinja2.env.globals['remove_subdomain'] = remove_subdomain

@app.get("/", response_class=HTMLResponse, name='index')
async def index(request: Request):
    return jinja2.TemplateResponse("index.html", {'request': request})


@app.get("/resume", response_class=HTMLResponse)
async def resume(request:Request):
    return jinja2.TemplateResponse("Carey,Connor-Resume.html", {'request': request})

