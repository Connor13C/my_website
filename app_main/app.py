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
    """
    Removes the subdomains off of a url path and returns only the hostname
    """
    url_list = value.split('.')
    domain = None
    if len(url_list) == 1:
        domain = url_list[-1]
    elif len(url_list) > 1:
        domain = '.'.join(url_list[-2:])
    return domain

jinja2.env.globals['remove_subdomain'] = remove_subdomain

@app.get("/", response_class=HTMLResponse, name='index')
async def index(request: Request):
    return jinja2.TemplateResponse("index.html", {'request': request})


@app.get("/resume", response_class=HTMLResponse)
async def resume(request:Request):
    return jinja2.TemplateResponse("Carey,Connor-Resume.html", {'request': request})

