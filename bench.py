

import time
import re

def bench(data):
    copy = "./writefile" 


    start = time.time()            
    regex = "Jul/2025:11:[345]\d"
    with open(copy, 'w') as writef:
        for line in data.split('\n'):
            if re.search(regex, line):
                #print(f"writeing {line}")
                writef.writelines(line)             

    end = time.time()
    return end - start