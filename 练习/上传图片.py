import os

import requests
import os
from Base.BasePath import BasePath as BP
from Base.baseYaml import read_yaml

file_path = os.path.join(BP.Data_Temp_Dir, 'img.png')

s = requests.session()

method = 'post'
url = 'https://imgbb.com/json'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42'
}
data = {
    'type': 'file',
    'action': 'upload',
    'timestamp': '1663897957030',
    'auth_token': '18eedeca88827d856ce28403be376117a991d912',
    'expiration': 'PT5M'
}


files = {
    'source': ('img.png', open(file_path, 'rb'), 'image/png')
}

res = s.request(method=method, url=url, headers=headers, data=data, files=files)
print(res.json())

