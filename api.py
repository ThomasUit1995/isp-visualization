import json
import datetime as dt
import pandas as pd

def read_file(file, dtFormat):
    df = None
    with open(file) as f:
        lines = f.read().splitlines()
        data = []
        for line in lines:
            if line:
                data.append(json.loads(line))
        df = pd.DataFrame(data)
        df['timestamp'] = df['timestamp'].apply(lambda x: dt.datetime.strptime(x, dtFormat))
    return df