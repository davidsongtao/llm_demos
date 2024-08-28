"""
Description: 日志管理系统配置文件，用于配置项目全局日志管理系统
    
-*- Encoding: UTF-8 -*-
@File     ：log_config.py
@Author   ：King Songtao
@Time     ：2024/8/28 上午9:25
@Contact  ：king.songtao@gmail.com
"""
from loguru import logger
import os
from pathlib import Path
from .basic_config import *

# 实例化全局参数配置
param = ParametersConfig()
log_directory = Path(param.log_directory)

# 检查日志存放目录是否存在，不存在则创建
if not log_directory.exists():
    log_directory.mkdir(parents=True, exist_ok=True)

# 通过环境变量获取日志级别，默认为INFO
log_level = os.getenv("LOG_LEVEL", "INFO")

# 配置日志的格式
# log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: 8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
# 配置一个日志处理器，用于将日志信息输出到文件中
logger.add(
    log_directory / "llm_demos_{time:YYYY-MM-DD_HH-MM}.log",
    rotation="2 hours",
    retention="10 days",
    compression="zip",
    level=log_level,
    format=log_format,
    enqueue=True
)
