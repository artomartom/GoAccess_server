import subprocess

 
import     settings  
import locale

locale.setlocale(locale.LC_ALL,'ru_RU.UTF-8')


def build_url(report_filename):
    return f"{ settings.HOSTNAME}/{report_filename}\n"

def get_log_format(sample_line): 
    return "COMBINED"
#  ^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(\d{2}\/[A-Za-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} [+\-]\d{4})\] "([A-Z]+) (\/[^ ]*) HTTP\/\d\.\d" (\d{3}) (\d+) "([^"]*)" "([^"]*)"$

def run_Goaccess( file_path, report_name): 
    
    format  = ""
    with open(file_path , 'r') as file:
        first_line = file.readline()
        format = get_log_format(first_line)

    args=  ['goaccess', file_path, "-a", "-o", f"{settings.REPORTS_DIR}/{report_name}", "--log-format", format ,  ]  # write to ././report.html
    #args=  ['goaccess', file_path, "-a", "-o", "html", "--log-format", "COMBINED",  ] # write to stdout

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
    