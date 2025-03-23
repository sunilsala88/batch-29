

import requests
TOKEN = '7956287339:AAH7mdFBkmsY0ngU2No5sCAWf6-n-bBwghg'
ids = '5563890177'

message='oder placed on goog at price 150'
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ids}&parse_mode=Markdown&text={message}"
print(requests.get(url).json())