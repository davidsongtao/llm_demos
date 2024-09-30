"""
Description: 主要用来定义查询数据库的函数，函数功能描述，以及函数的应用。
    
-*- Encoding: UTF-8 -*-
@File     ：sql_function_tools.py
@Author   ：King Songtao
@Time     ：2024/9/30 上午9:35
@Contact  ：king.songtao@gmail.com
"""
import json

import pymysql

# TODO 描述数据库表结构
database_schema_string = """
    CREATE TABLE 'emp'(
    'emp no' int DEFAULT NULL, --员工编号，默认为空
    `ename` varchar(50) DEFAULT NULL, --员工姓名,默认为空
    `job` varchar(50) DEFAULT NULL,--员工工作,默认为空
    `mgr` int DEFAULT NULL,--员工领导,默认为空
    `hiredate` date DEFAULT NULL,--员工入职日期,默认为空
    `sal` int DEFAULT NULL,--员工的月薪,默认为空
    `comm` int DEFAULT NULL,--员工年终奖,默认为空
    `deptno` int DEFAULT NULL,--员工部分编号,默认为空
    );
    CREATE TABLE `DEPT` (
    `DEPTNO` int NOT NULL, --部门编码,默认为空
    `DNAME` varchar(14) DEFAULT NULL,--部门名称,默认为空
    `LOC` varchar(13) DEFAULT NULL,--地点,默认为空
    PRIMARY KEY (`DEPTNO`)
);"""


# TODO 自定义数据库查询函数
def query_database(query):
    """传入sql语句，从数据库中查询结果"""
    # 1.连接到MYSQL数据库
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="1022",
            database="my_database",
            charset="utf8mb4",
        )
        print(f"连接成功！")
    except Exception as e:
        print(f"无法连接到数据库。错误信息：{e}")

    # 2.创建游标
    cursor = conn.cursor()
    print(f"创建游标成功！")

    # 3.执行sql语句测试
    # sql = "SELECT * FROM emp"
    cursor.execute(query)
    result = cursor.fetchall()
    print("执行测试成功！")

    # 4. 关闭游标，关闭连接
    cursor.close()
    conn.close()

    return result


# TODO 自定义解析模型返回结果的函数
def parse_response(response):

    response_message = response.choices[0].message

    if response_message:
        function_to_call = {"query_database": query_database}
        function_name = response.choices[0].message.tool_calls[0].function.name
        function_args = json.loads(response.choices[0].message.tool_calls[0].function.arguments)

        function_result = function_to_call[function_name](function_args.get("query"))

        return function_result
