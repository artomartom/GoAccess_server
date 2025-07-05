import subprocess


import   settings  

REPORTS_DIR = settings.REPORTS_DIR


def run_Goaccess( file_path, report_name): 
    args=  ['goaccess', file_path, "-a", "-o", f"{REPORTS_DIR}/{report_name}", "--log-format", "COMBINED",  ]  # write to ././report.html
    #args=  ['goaccess', file_path, "-a", "-o", "html", "--log-format", "COMBINED",  ] # write to stdout
    
 
    result =  subprocess.run(
        args,
        capture_output=True,
        encoding="utf-8",
        text=True
    )
    return result 
    