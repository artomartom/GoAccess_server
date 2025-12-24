import tempfile
from fastapi import FastAPI, APIRouter, Request, Query, status # type: ignore
from fastapi.responses import HTMLResponse,  RedirectResponse, JSONResponse # type: ignore
from fastapi.exceptions import HTTPException # type: ignore
from fastapi.templating import Jinja2Templates # type: ignore
import uvicorn # type: ignore

from settings import Settings
from utility import Logger as log
from report_generator import run_goaccess,new_report_id
from database import Database, preprocess_file
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

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    heading ='''Page not found'''
    error_text = "Error 404: Page not found"
    return await from_template(request,context = { "heading": heading,
                                    "text": str(error_text),
                                    "icon": "⚠️",
                                    }, status_code=404)

@app.exception_handler(405)
async def method_not_allowed(request: Request, exc: HTTPException):
    headers = {}
    headers["Allow"] = 'GET POST'

    return JSONResponse(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        content={"error": "Method not allowed", "allowed methods": 'GET POST'},
        headers=headers
    )

@routes.get("/")
async def redirect_home():
    return RedirectResponse(f"{Settings.external_url}/help")

@routes.get("/help", response_class=HTMLResponse)
async def get_help(request: Request):
    return await from_template(request,context = { "heading": '''Help''',
                                    "text": "Когда-нибудь тут будет документация",
                                    "icon": "❔❔❔",
                                    }, status_code=200)

@routes.get("/generate/{file_id}", response_class=HTMLResponse)
async def generate(request: Request,
                    file_id: str ):
    return templates.TemplateResponse(
        request=request, name="loading.html",context = { "file_id": file_id}, status_code=200)

@routes.get("/api/generate/{file_id}", response_class=HTMLResponse)
async def _generate(request: Request,
                    file_id: str
                    ):
    try:
        allowed_args = ["mth", "fmt","trnslt"]
        args = dict.fromkeys(allowed_args)
        args.update({key: value for key, value in dict(request.query_params).items() if key in allowed_args})

        log.debug(f"received args \n\t\t: {args}")

        ca = Cache_Server()
        cache_key = f"{file_id}/{args['mth']}/{args['fmt']}/{args['trnslt']}"
        cache = ca.get(cache_key)
        if cache is not  None:
            log.info(f"cache found for {cache_key}")
            return HTMLResponse(content=cache , status_code=200)
        db = Database()
        if db.id_exists(file_id) is False:
            raise FileNotFoundError(f"file '{file_id}' not found")


        with db.get_logfile(file_id) as data:
            test_chunk = data.readlines(200)# reads chars. CHANGE TO 200 LINES
            data.seek(0)

            fmt = Format.get_format(test_chunk, name=args['fmt'])
            args['fmt'] = fmt.name

            with tempfile.NamedTemporaryFile('w') as preprocessed_log:
                result:str=None
                if args['mth']:
                    preprocess_file(data,preprocessed_log,args)
                    result = run_goaccess(preprocessed_log.name, fmt)
                else:
                    result = run_goaccess(data.name, fmt)

                ca.set(cache_key,result)
                return HTMLResponse(content=result, status_code=200)

    except FileNotFoundError as error_text:
        heading ='''File Not Found'''
        return await from_template(request,context = { "heading": heading,
                                            "text": str(error_text),
                                            "icon": "⚠️",
                                            }, status_code=404)

    except Format.Exception as error_text:
        heading ='''Unknown Format Error'''
        description = '''Неизвестный или неподдерживаемый формат в вашем запросе.
                                Проверьте спецификацию формата и повторите попытку.'''
        return await from_template(request,context = { "heading": heading,
                                            "description": description,
                                            "text": str(error_text),
                                            "icon": "⚠️",
                                            }, status_code=400)

@routes.post("/upload")
async def upload( request: Request):
    try:
        file_id = new_report_id()


        log.debug (f"report file name {file_id}")
        url = f"{Settings.external_url}/generate/{file_id}"

        db = Database()

        contentlength = request.headers.get("content-length")


        if contentlength ==  '0':
            raise EOFError("Empty file")

        log.debug("writing data")
        await db.add_logfile_async(file_id,request)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={'report': url, 'status': 'OK'}
        )

    except EOFError as e:
        log.error(repr(e))
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'status': 'error',
                'message': "The file is empty"}
        )
    except Exception as e:
        log.error(repr(e))
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'status': 'error',
                'message': "Something went wrong"}
        )

@routes.get("/{path_name:path}")
async def redirect_get(request: Request, path_name: str):
    return await not_found_handler(request,HTTPException(status_code=404, detail="page not found"))

@routes.post("/{path_name:path}")
async def redirect_upload(request: Request, path_name: str):
    full_url = str(request.url.path)
    return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND ,
            content = { "Error 404": f"Page {full_url} not found ⚠️",
                        "redirect to": f"{Settings.external_url}/upload"}
        )

app.include_router(routes)

if __name__ == '__main__':
    uvicorn.run(
        app="app:app",
        port=Settings.port,
        workers= 1 if Settings.debug  else Settings.worker ,
        log_level=Settings.loglevel,
        access_log=True,
        timeout_keep_alive=5,
        host=Settings.listen)
