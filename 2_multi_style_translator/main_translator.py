"""
Description: 基于星火大模型的多风格翻译机
    
-*- Encoding: UTF-8 -*-
@File     ：main_translator.py
@Author   ：King Songtao
@Time     ：2024/9/18 下午8:49
@Contact  ：king.songtao@gmail.com
"""
import time
import sys

sys.path.append(r"d:\anaconda\envs\llm_demos\lib\site-packages")
from langchain.llms import Tongyi
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# 前端页面
import streamlit as st


def get_response(prompt, memory):
    """通过API调用大模型"""
    API_KEY = "your_api_key"
    try:
        model = Tongyi(
            model="qwen-max",
            api_key=API_KEY
        )
        chain = ConversationChain(llm=model, memory=memory)
        response = chain.invoke({"input": prompt})
        return response['response']
    except Exception as e:
        print(f"调用大模型时发生错误！错误代码：{e}")


def generate_res(res):
    """前端实现流式输出效果"""
    for char in res:
        yield char
        time.sleep(0.02)


style_selection = st.radio("", ["默认风格", "古文风格", "学术风格", "琼瑶风格"], horizontal=True)

if "history" not in st.session_state:
    st.session_state['history'] = ConversationBufferMemory()
    st.session_state["messages"] = [
        {
            "role": "ai",
            "content": "您好, 我是多风格翻译官小星, 很荣幸为您服务。我可以帮你将英文翻译成任意风格的中文，选择您偏好的风格，输入英文给我就可以啦~ :sunglasses:"
        }
    ]
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input("请输入您要翻译的内容，我将帮您翻译成中文...")
if prompt:

    if style_selection == "默认风格":
        style = '。 '
    elif style_selection == "古文风格":
        style = ', 请按照古文风格进行翻译, 用古诗词的行文风格, 做到辞藻精炼, 可用典故。'
    elif style_selection == "学术风格":
        style = ', 请按照学术风格进行翻译, 保持严谨认真的风格。'
    elif style_selection == "琼瑶风格":
        style = ', 请按照琼瑶风格进行翻译, 意境优美, 充满诗情画意, 或多愁善感, 或心花怒放。'
    else:
        style = '。'
    content = f"'{prompt}'" + "\n\n请将上述单引号内的英文内容翻译为中文,请不要瞎编乱造，只按风格进行翻译即可" + style
    uer_message = {
        "role": "user",
        "content": content
    }

    user_message_history = {
        "role": "user",
        "content": prompt
    }

    st.session_state['messages'].append(user_message_history)
    st.chat_message("human").write(prompt)

    with st.spinner("小星正在思考中，请稍等..."):
        response = get_response(content, memory=st.session_state['history'])

    stream_res = generate_res(response)
    ai_message = {
        "role": "ai",
        "content": response
    }

    st.session_state['messages'].append(ai_message)
    st.chat_message("ai").write(stream_res)
