#!/usr/bin/python3


import subprocess

if __name__=='__main__':
    args=  ['goaccess', "/home/artom/goaccess/half_meg.log", "-a", "-o", "./report.html", "--log-format", "COMBINED",  ]  # write to ././report.html
            #args=  ['goaccess', file_path, "-a", "-o", "html", "--log-format", "COMBINED",  ] # write to stdout

    #return subprocess.CompletedProcess( args , 0, "stdout", "stderr")


    result =  subprocess.run(
        args,
        capture_output=True,
        encoding="utf-8",
        text=True
    )

    print(result.stderr ) 
