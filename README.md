# 调用高德Web API demo

需求分析：收集六运小区周边餐饮、生活、购物场景的数据以及交通态势信息

`config.py`：基本参数设置，将自己申请的key导入

`request_poi.py`：收集周边餐饮、生活、购物场景的数据，需要先创建excel

`request_graph.py`：以上述抓取的poi数据为基础，以半径50m为单位申请高清静态图

`request_traffic.py`：每半小时抓取一次六运小区周边的交通态势信息，并将数据写入excel

如何将代码运行起来：申请高德Web API key，当前目录下创建surround_data.xlsx、road_data.xlsx文件

**具体请求格式可参考**：https://lbs.amap.com/api/webservice/summary/