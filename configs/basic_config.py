"""
Description: 全局参数配置文件，用于配置项目全局参数
    
-*- Encoding: UTF-8 -*-
@File     ：basic_config.py
@Author   ：King Songtao
@Time     ：2024/8/28 上午9:21
@Contact  ：king.songtao@gmail.com
"""
import torch.cuda


class ParametersConfig(object):
    def __init__(self):
        self.phone_price_data = r"D:\Projects\llm_demos\data\phone_price.csv"
        self.log_directory = r"D:\Projects\llm_demos\logs"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.lr = 1e-3
        self.epoch = 3000
        self.save_model = f'D:\\Projects\\llm_demos\\1_phone_price_prediction\\models\\phone_best_model.pth'
