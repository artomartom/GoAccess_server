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

from cache import Cache_Server

app = FastAPI(debug=DEBUG, docs_url=None, redoc_url=None)
error_page= """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>{text} HTML!</h1>
        </body>
    </html>
    """
 
 
 
@app.get("/v1/download/{file_id}", response_class=FileResponse) 
async def get_report_download(file_id: str, match: str = Query("")):
    res = await get_report(file_id,match)
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
                    match: str = Query("")):
    try: 
        
        ca = Cache_Server()
        cache = ca.get(f"{file_id}/{match}")
        if cache != None:
            logger(f"cache found for {file_id}/{match}")
            return HTMLResponse(content=cache , status_code=200)

        db = Database()
        logger(f"found match argument: {match}")

        if db.id_exists(file_id) == False:
            raise Exception(f"file {file_id} not found")
        data = db.get_logfile(file_id)  

        data = match_regex(match, data)

        result =  run_goaccess(data )

        ca.set(f"{file_id}/{match}",result)

        return HTMLResponse(content=result , status_code=200)
    
    except Exception as e:
        return HTMLResponse(content=error_page.format(text = str(e) ), status_code=500)

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
        #reload=True,     # Enable auto-reload for development
        workers=1,       # Number of worker processes (1 for development)
        log_level="info",  # Logging level
        access_log=True,   # Enable access logs
        timeout_keep_alive=5,  
                host=LISTEN)
