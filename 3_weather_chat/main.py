"""
Description: 具备查询实时天气的聊天机器人(天气查询为国家气象局提供的方法，每个城市有个ID，存在json文件中)
    
-*- Encoding: UTF-8 -*-
@File     ：main.py
@Author   ：King Songtao
@Time     ：2024/9/21 下午8:40
@Contact  ：king.songtao@gmail.com
"""
from zhipuai import ZhipuAI
import json
import requests

ZHIPU_API_KEY = ""
client = ZhipuAI(api_key=ZHIPU_API_KEY)

