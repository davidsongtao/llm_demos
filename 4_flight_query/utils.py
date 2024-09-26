"""
Description: 该文件定义了所有需要调用的外部工具类，如查询航班号，票价等
    
-*- Encoding: UTF-8 -*-
@File     ：utils.py
@Author   ：King Songtao
@Time     ：2024/9/25 上午9:27
@Contact  ：king.songtao@gmail.com
"""
import json


def get_flight_no(departure_city, arrival_city, date):
    """根据始发地，目的地及日期查询航信息"""
    try:
        flight_no = {
            "郑州": {
                "北京": "CA2549",
                "深圳": "GB9876",
                "广州": "SAZ497"
            },
            "北京": {
                "天津": "FG1123",
                "上海": "SHA976"
            }
        }

        flight_info = {"date": date, "flight_number": flight_no[departure_city][arrival_city]}
        return flight_info
    except Exception as e:
        return None


def get_ticket_price(date, flight_no):
    """根据日期及航班号，查询票价"""
    flight_info = {"tickets_price": "668"}
    return flight_info


def parse_function_call(model_response):
    pass
