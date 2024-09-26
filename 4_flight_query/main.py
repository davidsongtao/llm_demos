"""
Description:

-*- Encoding: UTF-8 -*-
@File     ：main.py
@Author   ：King Songtao
@Time     ：2024/9/26 上午11:07
@Contact  ：king.songtao@gmail.com
"""
import json

from zhipuai import ZhipuAI
from tools import *
from utils import *


def llm_query(message, tools=None, tool_choice="auto"):
    """调用大模型API，传入prompt,获取模型返回结果"""
    ZHIPU_API_KEY = "your_api_key"
    client = ZhipuAI(api_key=ZHIPU_API_KEY)
    ChatGLM = "glm-4"
    try:
        print("系统正在查询，请稍后...")
        response = client.chat.completions.create(
            model=ChatGLM,
            messages=message,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
    except Exception as e:
        print(f"与模型交互时发生错误。错误信息：{e}")
        return e


def parse_response(response):
    assistant_message = response.choices[0].message
    if assistant_message.tool_calls[0]:
        function_name = assistant_message.tool_calls[0].function.name
        function_arguments = assistant_message.tool_calls[0].function.arguments
        available_functions = {
            "get_flight_no": get_flight_no,
            "get_ticket_price": get_ticket_price
        }
        args = json.loads(function_arguments)
        function_result = available_functions[function_name](**args)
        return function_result


def main(query):
    messages = [
        {"role": "system", "content": "现在你是一个航班查询助手，将根据用户问题提供答案，但是不要假设或猜测传入函数的参数值。如果用户的描述不明确，请要求用户提供必要信息"},
        {"role": "user", "content": query}
    ]
    try:
        response = llm_query(messages, tools=tools, tool_choice="auto")
        assistant_message = response.choices[0].message
        tool_call_id = assistant_message.tool_calls[0].id
        messages.append(assistant_message.model_dump())
        function_result = str(json.dumps(parse_response(response)))
        if function_result == "null":
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": None,
                    "content": "没有查询到任何结果，请直接输出没有查询到结果。不要瞎编乱造。",
                }
            )
            second_response = llm_query(messages, tools=tools, tool_choice="auto")
            return second_response.choices[0].message.content

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": function_result,
            }
        )
        # try:
        second_response = llm_query(messages, tools=tools, tool_choice="auto")
        assistant_message_2 = second_response.choices[0].message
        if assistant_message_2.tool_calls == None:
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": None,
                    "content": "没有查询到任何票价结果。请忽略票价，回答用户的问题。不要瞎编乱造。",
                }
            )
            second_response = llm_query(messages, tools=tools, tool_choice="auto")
            return second_response.choices[0].message.content
        tool_call_id_2 = assistant_message_2.tool_calls[0].id
        messages.append(assistant_message_2.model_dump())
        function_result_2 = str(json.dumps(parse_response(second_response)))
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call_id_2,
                "content": function_result_2,
            }
        )
        final_response = llm_query(messages, tools=tools, tool_choice="auto")
        output = final_response.choices[0].message.content
        return output
    except Exception as e:
        return f"查询过程中出现错误，请检查您的查询后重试。"


if __name__ == '__main__':

    print(f"AI助手>>> 你好我是你的航班查询小助手。请输入您要查询的问题，我将帮助您查询。")
    while True:
        query = input("请输入您要查询的信息>>> ")
        output = main(query)
        print(f"AI助手>>> {output}")
