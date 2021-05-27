import json
import config
import requests
import pandas as pd
from openpyxl import load_workbook
from requests.exceptions import RequestException

def request_url(url):
    try:
        re = requests.get(url=url, timeout=30)
        if re.status_code == 200:
            return re.text
        return None
    except RequestException:
        print('Error for requesting url')
        return None

def parse_json(content):
    return json.loads(content)

def filter(data, sheet, row):
    extract = list()
    for item in data['pois']:
        extract.append([item['name'], item['type'], item['location'], item['address'], item['distance']])
    
    #写入excel
    frame = pd.DataFrame(extract)
    #frame.to_excel("extract_data.xlsx", sheet_name='餐饮', index=False) 会覆盖原有数据

    #读取被写入的excel
    book = load_workbook("surround_data.xlsx")
    #建立写入对象
    writer = pd.ExcelWriter("surround_data.xlsx", engine='openpyxl')
    writer.book = book
    writer.sheets = {ws.title: ws for ws in book.worksheets}
    frame.to_excel(writer, sheet_name=sheet, index=False, header=False, startrow=row)
    #writer.save()会导致打开excel有问题，换成close()可解决
    writer.close()

def rotate(url, sheet):
    last_row = 1
    for i in range(1, 20):
        #高德poi数据通过页数控制，默认一页20项数据，如果某页数据不足二十项则代表数据无了
        type_json = request_url(url + str(i))
        type_dic = parse_json(type_json)
        filter(type_dic, sheet, last_row)

        nums = len(type_dic['pois'])
        if nums < 20:
            break
        last_row += nums

key = config.key
url = config.url_data + '&types=' + config.life_poi + '&location=' + config.location + '&radius=200&page='
rotate(url, '生活')     #生活、购物、餐饮