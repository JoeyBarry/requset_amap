import os
import json
import config
import requests
import pandas as pd
from openpyxl import load_workbook
from requests.exceptions import RequestException

def read_key():
    key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'key.txt')
    with open(key_path, 'r', encoding='utf-8') as f:
        key = f.read()
    return key

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
    book = load_workbook("surround_data_1.xlsx")
    #建立写入对象
    writer = pd.ExcelWriter("surround_data_1.xlsx", engine='openpyxl')
    writer.book = book
    writer.sheets = {ws.title: ws for ws in book.worksheets}
    frame.to_excel(writer, sheet_name=sheet, index=False, header=False, startrow=row)
    #writer.save()会导致打开excel有问题，换成close()可解决
    writer.close()

def rotate(url, sheet):
    last_row = 1
    for i in range(1, 20):
        type_json = request_url(url + str(i))
        type_dic = parse_json(type_json)
        filter(type_dic, sheet, last_row)

        nums = len(type_dic['pois'])
        if nums < 20:
            break
        last_row += nums

# key = config.key
# url = config.url_data + '&types=' + config.life_poi + '&location=' + config.location + '&radius=200&page='
# rotate(url, '生活')

# test
# data = request_url(config.url_data + '&types=' + config.shopping_poi + '&location=' + config.location + '&radius=200&page=1')
# print(data)