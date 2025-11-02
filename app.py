import tempfile
import jinja2
from fastapi import FastAPI, APIRouter, Request, Query
from fastapi.responses import FileResponse, HTMLResponse,  RedirectResponse
from fastapi.exceptions import RequestValidationError, HTTPException
import uvicorn

from settings import Settings
from utility import Logger as log
from report_generator import run_goaccess,   new_report_id
from database import Database, filter_file_in_batches
from format_parser import  Format
from cache import Cache_Server

app = FastAPI(debug=Settings.debug, docs_url=None, redoc_url=None)
routes = APIRouter()

@app.middleware("http")
async def redirect_multiple_slashes(request: Request, call_next):
    path = request.url.path
    if path.startswith("//"):
        normalized_path = "/" + path.lstrip("/")
        return RedirectResponse(url=normalized_path)
    
    response = await call_next(request)
    return response

@routes.get("/download/{file_id}", response_class=FileResponse)
async def download(file_id: str,
                    mth: str = Query(""),
                    fmt: str = Query("")):
    res = await generate(file_id,mth,fmt)
    if res.status_code == 200:
        headers = {"Content-disposition": "attachment" }
        return HTMLResponse(content=res.body, status_code = res.status_code,headers=headers )
    return res


@routes.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    with open("assets/message_page.html", 'r',encoding='utf-8') as file:
        html_page = file.read()
        heading ='''404'''
        error_text = "Not Found"
        html_page = jinja2.Template(html_page).render(icon = "⚠️", heading=heading, text = error_text)
        return HTMLResponse(
            content=html_page,
            status_code=404
        )

@routes.get("/")
async def redirect_home():
    return RedirectResponse(f"{Settings.external_url}/help")

@routes.get("/help", response_class=HTMLResponse)
async def get_help():
    with open("assets/message_page.html", 'r',encoding='utf-8') as file:
        html_page = file.read()
        heading ='''Help'''
        html_page = jinja2.Template(html_page).render(icon = "❔❔❔",heading=heading, text = "This is a help page")
        return HTMLResponse(html_page, status_code=200)

@routes.get("/generate/{file_id}", response_class=HTMLResponse)
async def generate(file_id: str,
                    mth: str = Query(""),
                    fmt: str = Query("")
                    ):
    try:
        log.verbose(f"received args \n\t\tmth: {mth}\n\t\tfmt: {fmt}")

        ca = Cache_Server()
        cache_key = f"{file_id}/{mth}/{fmt}"
        cache = ca.get(cache_key)
        if cache is not  None:
            log.info(f"cache found for {cache_key}")
            return HTMLResponse(content=cache , status_code=200)
        db = Database()
        log.verbose(f"found match argument: {mth}")
        if db.id_exists(file_id) is False:
            raise FileNotFoundError(f"file '{file_id}' not found")


        with db.get_logfile(file_id) as data:
            test_chunk = data.readlines(200)# reads chars. CHANGE TO 200 LINES
            data.seek(0)

            fmt = Format.get_format(test_chunk, name=fmt)
            data.seek(0)
            if mth != "":
                with tempfile.NamedTemporaryFile('w') as parsed_log:
                    filter_file_in_batches(data,parsed_log,mth)
                    result =  run_goaccess(parsed_log.name,fmt )
                    ca.set(cache_key,result)
                    return HTMLResponse(content=result , status_code=200)

            result =  run_goaccess(data.name ,fmt )
            ca.set(cache_key,result)
            return HTMLResponse(content=result , status_code=200)

    except FileNotFoundError as e:
        with open("assets/message_page.html", 'r',encoding='utf-8') as file:
            html_page = file.read()
            heading ='''File Not Found'''
            error_text = str(e)
            html_page = jinja2.Template(html_page).render(icon = "⚠️", heading=heading, text = error_text)
            return HTMLResponse(html_page, status_code=404)

    except Format.Exception as e:
        with open("assets/message_page.html", 'r',encoding='utf-8') as file:
            html_page = file.read()
            heading ='''Unknown Format Error'''
            description = '''The server encountered an unknown or unsupported format in your request.
                        Please check the format specification and try again.'''
            error_text = str(e)

            html_page = jinja2.Template(html_page).render(icon = "⚠️", heading=heading,description=description,text = error_text)
            return HTMLResponse(html_page, status_code=400)


@routes.post("/report")
async def get_report( request: Request):
    return await  upload(request)

@routes.post("/upload")
async def upload( request: Request):
    try:
        file_id = new_report_id()


        log.verbose (f"report file name {file_id}")
        url = f"{Settings.external_url}/generate/{file_id}"

        db = Database()

        _, contentlength = request._headers._list[5]

        if contentlength.decode() ==  '0':
            raise EOFError("Empty file")

        log.verbose("writing data")
        await db.add_logfile_async(file_id,request)

        return  {
            'report': url ,
            'status': 'OK' 
        }

    except EOFError as e:
        log.error(repr(e))
        return  {
            'status': 'error',
            'message': "The file is empty"
        }
    except Exception as e:
        log.error(repr(e))
        return  {
            'status': 'error',
            'message': "Something went wrong"
        }

app.include_router(routes)

if __name__ == '__main__':
    uvicorn.run(
        app="app:app",
        port=Settings.port,
        workers= 1 if Settings.debug  else Settings.worker ,
        log_level="info",
        access_log=True,
        timeout_keep_alive=5,
        host=Settings.listen)
