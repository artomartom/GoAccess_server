from fastapi import FastAPI, Request, Query
from fastapi.responses import FileResponse, HTMLResponse
import uvicorn

from settings import LISTEN,  DEBUG, PORT, VERSION, HOSTNAME
from utility import  logger
from report_generator import run_goaccess,   new_report_id
from database import Database
import time
import re
import io
import jinja2
from  format_parser import  Format

from cache import Cache_Server

app = FastAPI(debug=DEBUG, docs_url=None, redoc_url=None)

@app.get("/v1/download/{file_id}", response_class=FileResponse) 
async def get_report_download(file_id: str, 
                    mth: str = Query(""),
                    fmt: str = Query("")):
    res = await get_report(file_id,mth,fmt)
    if res.status_code == 200:
        headers = {"Content-disposition": "attachment" }
        return HTMLResponse(content=res.body, status_code = res.status_code,headers=headers )
    return res

def match_regex(match: str, data: str):
    if match == ""  :
        return data
        
    new_data="" 
    for line in data.split('\n'):
        if re.search(match, line):
            new_data+=line  
            new_data+='\n' 
    return  new_data
 
@app.get("/v1/generate/{file_id}", response_class=HTMLResponse) 
async def get_report(file_id: str,
                    mth: str = Query(""),
                    fmt: str = Query("")
                    ):
    try:
        
        logger(f"received args \n\t\tmth: {mth}\n\t\tfmt: {fmt}") 
        
        ca = Cache_Server()
        cache_key = f"{file_id}/{mth}/{fmt}"
        cache = ca.get(cache_key)
        if cache != None:
            logger(f"cache found for {cache_key}")
            return HTMLResponse(content=cache , status_code=200)
        db = Database()
        logger(f"found match argument: {mth}")
        if db.id_exists(file_id) == False:
            raise Exception(f"file {file_id} not found")
            ##TODO FileNotFoundError expection with error page html
        data = db.get_logfile(file_id)  

        fmt = Format.get_format(data.split('\n', 200), name=fmt)
    
        data = match_regex(mth, data)
        
        result =  run_goaccess(data ,fmt )
        ca.set(cache_key,result)
        return HTMLResponse(content=result , status_code=200)
    
    except Format.Exception as e:
        with open("error_page.html", 'r') as file:
            html_page = file.read()
            error_text = str(e) #.replace("\n","\n\t")
            html_page = jinja2.Template(html_page).render(error_text = error_text)
            return HTMLResponse(html_page, status_code=500)

@app.post("/v1/report") 
async def get_report1( request: Request): 
    return await  get_upload(request)
 
@app.post("/v1/upload") 
async def get_upload( request: Request): 
    try: 
        start = time.time()
        file_id = new_report_id()
        

        logger (f"report file name {file_id}")
        url = f"{HOSTNAME}/v1/generate/{file_id}" 
        
        db = Database()

        data =  await request.body()
        
        if len(data) ==  0:
            raise Exception("Empty file")
        
        logger(f"writing  data")
        db.add_logfile(file_id,data)

        return  {
            'report': url ,
            'status': 'OK',
            'version': VERSION,
            'time' :  time.time() - start
        }

    except Exception as e:
        return  {
            'status': 'error',
            'message': str(e),
            'version': VERSION
        }

 

if __name__ == '__main__':
    uvicorn.run( 
        app="app:app",  # Path to your FastAPI app (module:app)
        port=int(PORT), 
        workers=1,       # Number of worker processes (1 for development)
        log_level="info",  # Logging level
        access_log=True,   # Enable access logs
        timeout_keep_alive=5,  
                host=LISTEN)

 