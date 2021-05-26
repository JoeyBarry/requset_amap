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

def read_sheet(sheet, column):
    frame = pd.read_excel('surround_data.xlsx', sheet_name=sheet)
    #frame.ix已经被重构成loc
    data = frame.loc[:, column]
    return data

def save_photo(name, bytes):
    with open(name, 'wb') as img:
        img.write(bytes)

sheet = '生活'  #餐饮、生活、购物
dir = 'photos/' + sheet + '/'   #保存图片位置
url = config.url_photo + '&markers=large,0xEE6363,:'
location, distance = read_sheet(sheet, '经纬度'), read_sheet(sheet, '距中心点距离（米）')

#以50米为半径，记录中间存在多少实体
counts = list()
record, count = 50, 0
for d in distance:
    if d <= record:
        count += 1
    elif d > 150:
        counts.append(count)
        record = 200
        count = 1
    elif d > 100:
        counts.append(count)
        record = 150
        count = 1
    elif d > 50:
        counts.append(count)
        record = 100
        count = 1
if count > 1:
    counts.append(count)

last_index, radius = 0, 50
for c in counts:
    name = '(' + str(radius - 50) + 'm-' + str(radius) + 'm' + ')'
    rotate_url, last_seq = url, 0
    for i in range(c):
        rotate_url += str(location[i + last_index])
        if (i + 1) % 50 != 0 and i != c - 1:
            rotate_url += ';'
        else:
            photo_bytes = request_url(rotate_url)
            save_photo(dir + name +  str(last_seq) + '-' + str(i) + 'life.png', photo_bytes)
            rotate_url = url
            last_seq = i + 1
    radius += 50
    last_index += c

# photo_bytes = request_url(rotate_url)
# save_photo(dir + str(len(location) - 1) + "shopping.png", photo_bytes)