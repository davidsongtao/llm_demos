"""
Description: 
    
-*- Encoding: UTF-8 -*-
@File     ：model.py
@Author   ：King Songtao
@Time     ：2024/8/28 上午10:38
@Contact  ：king.songtao@gmail.com
"""
import torch.nn as nn
import torch


class PhonePriceModel(nn.Module):
    def __init__(self):
        super(PhonePriceModel, self).__init__()
        # 第一层，输入维度20，输出维度：128
        self.linear1 = nn.Linear(20, 512)
        # 第二层，输入维度128，输出维度256
        self.linear2 = nn.Linear(512, 1024)
        # 增加一层
        # self.linear3 = nn.Linear(256, 512)
        # 第三层，输入维度256，输出维度4
        self.linear3 = nn.Linear(1024, 4)

    def forward(self, x):
        x = torch.relu(self.linear1(x))
        x = torch.relu(self.linear2(x))
        # x = torch.relu(self.linear3(x))
        output = self.linear3(x)
        return output
