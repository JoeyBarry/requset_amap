import json
import time
import config
import requests
import pandas as pd
from openpyxl import load_workbook
from requests.exceptions import RequestException

def request_url(url):
    try:
        rq = requests.get(url)
        print(rq.status_code, rq)
        if rq.status_code == 200:
            return rq.text
        return None
    except RequestException:
        return None

def parse_json(content):
    return json.loads(content)

def filter(data, sheet, row):
    single_dimension = list()
    extract_info = data['trafficinfo']
    single_dimension.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    single_dimension.append(extract_info['description'])
    single_dimension.append(extract_info['evaluation']['expedite'])
    single_dimension.append(extract_info['evaluation']['congested'])
    single_dimension.append(extract_info['evaluation']['blocked'])
    single_dimension.append(extract_info['evaluation']['unknown'])
    for road in extract_info['roads']:
        single_dimension.append(road['direction'])
        if road['status'] == '0':
            single_dimension.append('未知')
        elif road['status'] == '1':
            single_dimension.append('畅通')
        elif road['status'] == '2':
            single_dimension.append('缓行')
        elif road['status'] == '3':
            single_dimension.append('拥堵')
        elif road['status'] == '4':
            single_dimension.append('严重拥堵')
        if 'speed' in road:
            single_dimension.append(road['speed'])
        else:
            single_dimension.append('暂无数据')
    second_dimension = list()
    second_dimension.append(single_dimension)
    write_to_excel(second_dimension, sheet, row)

def write_to_excel(extract_data, sheet, row):
    print(extract_data)
    frame = pd.DataFrame(extract_data)
    book = load_workbook("road_data.xlsx")
    writer = pd.ExcelWriter("road_data.xlsx", engine='openpyxl')
    writer.book = book
    writer.sheets = {ws.title: ws for ws in book.worksheets}
    frame.to_excel(writer, sheet_name=sheet, index=False, header=False, startrow=row)
    writer.close()


start_row = 1
while True:
    sheets = ['体育西路', '天河南一路', '体育西横街'] #天河南一路、体育西横街、体育西路
    for sheet in sheets:
        url = config.url_road + '&extensions=all&name=' + sheet
        traffic_json = request_url(url)
        traffic_dic = parse_json(traffic_json)
        filter(traffic_dic, sheet, start_row)
    start_row += 1
    time.sleep(1800)