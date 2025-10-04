from fastapi import FastAPI, Request, Query
from fastapi.responses import FileResponse, HTMLResponse
import uvicorn
from settings import Settings
from utility import Logger as log
from report_generator import run_goaccess,   new_report_id
from database import Database, filter_file_in_batches
import time
import io
import jinja2
from  format_parser import  Format
import tempfile

from cache import Cache_Server

app = FastAPI(debug=Settings.debug, docs_url=None, redoc_url=None)

@app.get("/v1/download/{file_id}", response_class=FileResponse) 
async def download(file_id: str, 
                    mth: str = Query(""),
                    fmt: str = Query("")):
    res = await generate(file_id,mth,fmt)
    if res.status_code == 200:
        headers = {"Content-disposition": "attachment" }
        return HTMLResponse(content=res.body, status_code = res.status_code,headers=headers )
    return res

 
@app.get("/v1/help", response_class=HTMLResponse) 
async def get_help():
    with open(f"assets/message_page.html", 'r') as file:
        html_page = file.read()
        heading ='''Help'''
        html_page = jinja2.Template(html_page).render(icon = "❔❔❔",heading=heading, text = "This is a help page")
        return HTMLResponse(html_page, status_code=200)
                     
@app.get("/v1/generate/{file_id}", response_class=HTMLResponse) 
async def generate(file_id: str,
                    mth: str = Query(""),
                    fmt: str = Query("")
                    ):
    try:
        log.verbose(f"received args \n\t\tmth: {mth}\n\t\tfmt: {fmt}") 
        
        ca = Cache_Server()
        cache_key = f"{file_id}/{mth}/{fmt}"
        cache = ca.get(cache_key)
        if cache != None:
            log.info(f"cache found for {cache_key}")
            return HTMLResponse(content=cache , status_code=200)
        db = Database()
        log.verbose(f"found match argument: {mth}")
        if db.id_exists(file_id) == False:
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
        with open(f"assets/message_page.html", 'r') as file:
            html_page = file.read()
            heading ='''File Not Found'''
            error_text = str(e)  
            html_page = jinja2.Template(html_page).render(icon = "⚠️", heading=heading, text = error_text)
            return HTMLResponse(html_page, status_code=404)
         
    except Format.Exception as e:
        with open(f"assets/message_page.html", 'r') as file:
            html_page = file.read()
            heading ='''Unknown Format Error'''
            description = '''The server encountered an unknown or unsupported format in your request.
                        Please check the format specification and try again.'''
            error_text = str(e)  
            
            html_page = jinja2.Template(html_page).render(icon = "⚠️", heading=heading,description=description,text = error_text)
            return HTMLResponse(html_page, status_code=400)
        

@app.post("/v1/report") 
async def get_report( request: Request): 
    return await  upload(request)
 
@app.post("/v1/upload") 
async def upload( request: Request): 
    try: 
        start = time.time()
        file_id = new_report_id()
        

        log.verbose (f"report file name {file_id}")
        url = f"{Settings.hostname}/v1/generate/{file_id}" 
        
        db = Database()

        _, contentlength = request._headers._list[5]
        
        if contentlength.decode() ==  '0':
            raise Exception("Empty file")
        
        log.verbose(f"writing data")
        await db.add_logfile_async(file_id,request)

        return  {
            'report': url ,
            'status': 'OK',
            'version': Settings.version,
            'time' :  time.time() - start
        }

    except Exception as e:
        log.error(repr(e))
        return  {
            'status': 'error',
            'message': str(e),
            'version': Settings.version
        }

 

if __name__ == '__main__':
    uvicorn.run( 
        app="app:app",  # Path to your FastAPI app (module:app)
        port=Settings.port, 
        workers= 1 if Settings.debug  else Settings.worker ,     
        log_level="info",  # Logging level
        access_log=True,   # Enable access logs
        timeout_keep_alive=5,  
                host=Settings.listen)

 
