"""
Description: 
    
-*- Encoding: UTF-8 -*-
@File     ：tools.py
@Author   ：King Songtao
@Time     ：2024/9/30 上午9:54
@Contact  ：king.songtao@gmail.com
"""
from sql_function_tools import database_schema_string
tools = [
    {
        "type": "function",
        "function": {
            "name": "query_database",
            "description": "使用此函数回答业务问题，要求输出是一个SQL查询语句",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": f"SQL查询提取信息以回答用户的问题。SQL应该使用以下数据库模式编写：{database_schema_string}。查询结果应该以JSON格式返回。查询应该只包含MySQL支持的语法。",
                    }
                },
                "required": ["query"],
            },
        }
    }
]