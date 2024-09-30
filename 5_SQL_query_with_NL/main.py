"""
Description: 通过自然语言查询SQL数据库中的数据。主逻辑函数，实现模型function call的调用
    
-*- Encoding: UTF-8 -*-
@File     ：main.py
@Author   ：King Songtao
@Time     ：2024/9/26 下午5:28
@Contact  ：king.songtao@gmail.com
"""
from zhipuai import ZhipuAI
from sql_function_tools import *
from tools import *


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


if __name__ == '__main__':
    message = [
        {"role": "system", "content": "通过查询业务数据库，针对其生成SQL查询来回答用户的问题"},
        {"role": "user", "content": "查询一下工资最低的员工是谁"}
    ]

    # 首次查询，获取结果，调用function
    response = llm_query(message, tools=tools)
    function_result = parse_response(response)
    message.append(
        response.choices[0].message.model_dump()
    )
    function_name = response.choices[0].message.tool_calls[0].function.name
    function_id = response.choices[0].message.tool_calls[0].id

    # 将函数调用结果重新组织放入历史数据
    message.append(
        {
            "role": "tool",
            "tool_call_id": function_id,
            "name": function_name,
            "content": f"{function_result}"
        }
    )

    # 融合函数调用结果后，第二次送入大模型进行查询，获取最终结果
    final_response = llm_query(message, tools=tools)
    print(f"AI助手 >>> {final_response.choices[0].message.content}")
