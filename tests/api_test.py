


import requests
import json

url = 'https://goaccess.suschkov.ru/upload'

log_file = [
'test.combined.log',
'test.combined_x_for.log',
'test.hestia.log',
'test.bitrix.log',
'test.badformat.log'
'test.empty.log',
]

log_dir = './'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def send_log(log_name:str):

    file =   open(f"{log_dir}/{log_name}", 'rb').read()
    requests.post(url, headers=headers, data=file)

    res = json.loads(response.text)
    print(json.dumps(res,indent=4))
    return response.status_code, res['report']

def get_report(url:str):
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    html_content = response.text
    print(f"Success! Received {len(html_content)} characters")

    with open('report.html', 'w', encoding='utf-8') as f:
        f.write(html_content)


if __name__ == '__main__':
    code, url = send_log(log_file[0])
    print( url)
    assert code == 200
    #get_report(url)
