import time
import re
import subprocess
def bench(data):
    copy = "./writefile" 


    start = time.time()            
    regex = "Jul/2025:11:[345]"
    with open(copy, 'w') as writef:
        for line in data.split('\n'):
            if re.search(regex, line):
                #print(f"writeing {line}")
                writef.writelines(line)             

    end = time.time()
    return end - start



if __name__ == '__main__':


    args =  ['goaccess', "/home/kiwi/logs/test.log" , "-a", "--log-format", "COMBINED" ] 

    result =  subprocess.run(
        args,
        capture_output=True,
        encoding="utf-8",
        text=True
    )
    
    print(result.stdout)






