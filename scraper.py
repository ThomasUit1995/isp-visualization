import json
import requests
import datetime as dt

address = 'localhost'
port = 8080
page = 'response'
url = f'http://{address}:{port}/{page}'
short = 'data/short.txt'
long = 'data/long.txt'

def get_stream(url, dtFormat):
    s = requests.Session()
    with open(short, 'r+') as f:
        f.truncate(0)
    with s.get(url, headers=None, stream=True) as resp:
        for line in resp.iter_lines():
            if line:
                parsedDict = json.loads(line.decode('utf-8'))
                parsedDict['timestamp'] = dt.datetime.now().strftime(dtFormat)
                strDict = json.dumps(parsedDict)
                with open(short, 'a') as fileShort:
                    fileShort.write(f'{strDict}\n')
                with open(long, 'a') as fileLong:
                    fileLong.write(f'{strDict}\n')

get_stream(url, '%Y-%m-%d %H:%M:%S')
