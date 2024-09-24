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


# TODO 第一步 -> 自定义get_current_weather函数
def get_current_weather(location):
    """得到给定地址的当前天气信息"""
    with open(r"D:\Projects\llm_demos\3_weather_chat\cityCode_use.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    city_code = ""

    for item in data:
        if item["城市"] == location:
            city_code = item["编码"]

    if city_code:
        weather_url = "http://t.weather.itboy.net/api/weather/city/" + city_code
        response = requests.get(weather_url)
        result = eval(response.text)
        current_weather = result['data']['forecast'][0]
        weather_info = {
            "location": location,
            "date": current_weather['ymd'],
            "high_temperature": current_weather['high'],
            "low_temperature": current_weather['low'],
            "wind": current_weather['fx'],
            "weather_type": current_weather['type'],
        }
    else:
        weather_info = {
            "error_message": "未找到该城市，暂无数据",
        }

    weather_info = json.dumps(weather_info, ensure_ascii=False)
    return weather_info


# TODO 第二步 -> 定义函数描述功能
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "根据给定城市，查询对应城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或区，例如北京、上海"
                    }
                },
                "required": ["location"]
            },
        }
    }
]


# TODO 第三步 -> 解析模型参数调用函数
def parse_response(response):
    """根据模型回复来确定是否调用工具函数，如果调用返回函数结果"""
    response_message = response.choices[0].message
    # print(f"response_message --> {response_message}")
    if response_message.tool_calls:
        available_functions = {
            "get_current_weather": get_current_weather
        }
        function_name = response_message.tool_calls[0].function.name
        function_to_call = available_functions[function_name]  # 这里如果等于None，说明不需要调用函数
        # print(f"function_to_call --> {function_to_call}")

        function_args = json.loads(response_message.tool_calls[0].function.arguments)
        function_response = function_to_call(location=function_args.get('location'))
        return function_response


def llm_query(message, tools=None, tool_choice=None):
    """调用大模型API，传入prompt,获取模型返回结果"""
    ZHIPU_API_KEY = "your_api_key"
    client = ZhipuAI(api_key=ZHIPU_API_KEY)
    ChatGLM = "glm-4"
    try:
        response = client.chat.completions.create(
            model=ChatGLM,
            messages=message,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
    except Exception as e:
        print(f"模型交互时发生错误。错误信息：{e}")
        return e


if __name__ == '__main__':

    # TODO 首次查询，将函数池做为参数传递给大模型
    messages = [{
        "role": "system",
        "content": "你是一个天气播报小助手，你需要根据用户提供的地址回答当前的天气情况，如果用户提供的问题具有不确定性，请不要自己编造内容，已使用户明确输入"
    }, {
        "role": "user",
        "content": "今天上海天气怎么样？"
    }]
    response = llm_query(messages, tools=tools, tool_choice="auto")
    # print(f"response --> {response}")

    # TODO 通过模型给出的首次回复，解析出需要调用哪些函数，并在后端进行调用
    function_response = parse_response(response)

    # TODO 将第一词查询时大模型返回的结果添加到消息列表中
    assistant_message = response.choices[0].message
    messages.append(assistant_message.model_dump())
    # print(f"assistant_message --> {assistant_message}")
    # print(f"function_response --> {function_response}")

    # TODO 进行第二次查询，将函数返回值做为参数传递给大模型
    function_name = response.choices[0].message.tool_calls[0].function.name
    function_id = response.choices[0].message.tool_calls[0].id
    messages.append(
        {
            "role": "tool",
            "tool_call_id": function_id,
            "name": function_name,
            "content": function_response
        }
    )
    # print(messages)
    last_response = llm_query(messages, tools=tools, tool_choice="auto")
    result = last_response.choices[0].message.content
    print(f"AI助手-->> {result}")
