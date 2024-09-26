"""
Description: 自定义函数描述功能
    
-*- Encoding: UTF-8 -*-
@File     ：tools.py
@Author   ：King Songtao
@Time     ：2024/9/26 上午11:18
@Contact  ：king.songtao@gmail.com
"""
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_flight_no",
            "description": "根据始发地,目的地和日期,查询对应日期的航班号",
            "parameters": {
                "type": "object",
                "properties": {
                    "departure_city": {
                        "description": "始发地",
                        "type": "string"
                    },
                    "arrival_city": {
                        "description": "目的地",
                        "type": "string"
                    },
                    "date": {
                        "description": "日期",
                        "type": "string"
                    }
                },
                "required": ["departure_city", "arrival_city", "date"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_ticket_price",
            "description": "查询某航班在某日的价格",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "description": "日期",
                        "type": "string"
                    },
                    "flight_no": {
                        "description": "航班号",
                        "type": "string"
                    }
                },
                "required": ["date", "flight_no"]
            }
        }
    }
]
