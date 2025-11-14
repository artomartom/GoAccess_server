import tempfile
from fastapi import FastAPI, APIRouter, Request, Query # type: ignore
from fastapi.responses import FileResponse, HTMLResponse,  RedirectResponse # type: ignore
from fastapi.exceptions import  HTTPException # type: ignore
from fastapi.templating import Jinja2Templates # type: ignore
import uvicorn # type: ignore

from settings import Settings
from utility import Logger as log
from report_generator import run_goaccess,   new_report_id
from database import Database, filter_file_in_batches
from format_parser import  Format
from cache import Cache_Server

app = FastAPI(debug=Settings.debug, docs_url=None, redoc_url=None)
routes = APIRouter()

templates = Jinja2Templates(directory="assets")

async def from_template(request: Request, context: dict,status_code:int):
    return templates.TemplateResponse(
        request=request, name="message_page.html", context=context,status_code=status_code)

@app.middleware("http")
async def redirect_multiple_slashes(request: Request, call_next):
    path = request.url.path
    if path.startswith("//"):
        normalized_path = "/" + path.lstrip("/")
        return RedirectResponse(url=normalized_path)

    response = await call_next(request)
    return response

@routes.get("/download/{file_id}", response_class=FileResponse)
async def download(request: Request,
                    file_id: str,
                    mth: str = Query(""),
                    fmt: str = Query("")):
    res = await generate(request,file_id,mth,fmt)
    if res.status_code == 200:
        headers = {"Content-disposition": "attachment" }
        return HTMLResponse(content=res.body, status_code = res.status_code,headers=headers )
    return res


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    heading ='''Page not found'''
    error_text = "Error 404: Page not found"
    return await from_template(request,context = { "heading": heading,
                                    "text": str(error_text),
                                    "icon": "⚠️",
                                    }, status_code=404)

@routes.get("/")
async def redirect_home():
    return RedirectResponse(f"{Settings.external_url}/help")

@routes.get("/help", response_class=HTMLResponse)
async def get_help(request: Request):
    return await from_template(request,context = { "heading": '''Help''',
                                    "text": "This is a help page",
                                    "icon": "❔❔❔",
                                    }, status_code=200)

@routes.get("/generate/{file_id}", response_class=HTMLResponse)
async def generate(request: Request,
                    file_id: str,
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

    except FileNotFoundError as error_text:
        heading ='''File Not Found'''
        return await from_template(request,context = { "heading": heading,
                                            "text": str(error_text),
                                            "icon": "⚠️",
                                            }, status_code=404)

    except Format.Exception as error_text:
        heading ='''Unknown Format Error'''
        description = '''The server encountered an unknown or unsupported format in your request.
                    Please check the format specification and try again.'''
        return await from_template(request,context = { "heading": heading,
                                            "description": description,
                                            "text": str(error_text),
                                            "icon": "⚠️",
                                            }, status_code=400)

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

        contentlength = request.headers.get("content-length")
        

        if contentlength ==  '0':
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
