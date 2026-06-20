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
    Removes the subdomains off of a url path and returns only the hostname. Works for localhost and production
    """
    url_list = value.split('.')
    if len(url_list) < 3:
        return url_list[-1]
    else:
        return '.'.join(url_list[-2:])

jinja2.env.globals['remove_subdomain'] = remove_subdomain

@app.get("/", response_class=HTMLResponse, name='index')
async def index(request: Request):
    return jinja2.TemplateResponse(request=request, name="index.html")


@app.get("/resume", response_class=HTMLResponse)
async def resume(request:Request):
    return jinja2.TemplateResponse(request=request, name="resume.html")

