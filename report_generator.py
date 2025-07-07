import subprocess

 
import     settings  



def build_url(report_filename):
    return f"{ settings.HOSTNAME}/{report_filename}\n"

def run_Goaccess( file_path, report_name): 
    args=  ['goaccess', file_path, "-a", "-o", f"{settings.REPORTS_DIR}/{report_name}", "--log-format", "COMBINED",  ]  # write to ././report.html
    #args=  ['goaccess', file_path, "-a", "-o", "html", "--log-format", "COMBINED",  ] # write to stdout
    
   # print (f"file_path {file_path}")
    #print (f"REPORTS_DIR  {settings.REPORTS_DIR}/{report_name}")
    print (f"running goaccess")
    print (f"file path {file_path}")
    print (f"report path  {settings.REPORTS_DIR}/{report_name}")
    result =  subprocess.run(
        args,
        capture_output=True,
        encoding="utf-8",
        text=True
    )
    return result 
    