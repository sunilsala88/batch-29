

import requests
TOKEN = ''
ids = ''

message='oder placed on goog at price 150'
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ids}&parse_mode=Markdown&text={message}"
print(requests.get(url).json())