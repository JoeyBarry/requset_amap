import config
import requests
import pandas as pd
from requests.exceptions import RequestException

def request_url(url):
    try:
        rq = requests.get(url=url)
        print(rq, rq.status_code)
        if rq.status_code == 200:
            # rq.text为str, rq.content为bytes
            return rq.content
        return None
    except RequestException:
        return None

def read_location(sheet):
    frame = pd.read_excel('extract_data.xlsx', sheet_name=sheet)
    #frame.ix已经被重构成loc
    location = frame.loc[:, '经纬度']
    return location

def save_photo(name, bytes):
    with open(name, 'wb') as img:
        img.write(bytes)

url = config.url_photo
times, nums = 1, 49
sheet = '购物'
dir = 'photos/' + sheet + '/'
location = read_location(sheet)
rotate_url = url
for i in range(len(location)):
    rotate_url += str(location[i])
    if times % (nums + 1) != 0:
        rotate_url += ';'
    else:
        photo_bytes = request_url(rotate_url)
        save_photo(dir + str(i - nums) + '-' + str(i) + "shopping.png", photo_bytes)
        rotate_url = url
    times += 1

# photo_bytes = request_url(rotate_url)
# save_photo(dir + str(len(location) - 1) + "shopping.png", photo_bytes)