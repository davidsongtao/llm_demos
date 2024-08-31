"""
Description: 手机几个预测案例实现，项目主要实现步骤如下：
                1).准备训练数据集 2).构建要使用的模型 3).模型训练 4).模型巨册评估
    
-*- Encoding: UTF-8 -*-
@File     ：main.py
@Author   ：King Songtao
@Time     ：2024/8/28 上午9:37
@Contact  ：king.songtao@gmail.com
"""
from torch.optim.lr_scheduler import StepLR

# 第1步 --> 导入必要的包
from configs.log_config import *  # 日志管理系统
from torch.utils.data import TensorDataset, DataLoader
from model import *
import torch.optim as optim
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import time


# 第2步 --> 准备训练数据集
def data_preprocess(file_path):
    """读取csv数据文件，创建数据集"""
    # 读取csv文件
    try:
        data = pd.read_csv(file_path)
        # 将csv文件数据进行切片，前20列作为特征值，最后一列作为目标值
        x, y = data.iloc[:, :-1], data.iloc[:, -1]
        # 特征值目标值类型转换
        if not all(data[col].dtype in [np.float64, np.int64] for col in data.columns):
            logger.warning("数据包含非数值类型，尝试转换")
        x = x.astype(np.float32)
        y = y.astype(np.int64)
        # 训练集验证机数据划分
        x_train, x_valid, y_train, y_valid = train_test_split(x, y, train_size=0.8, random_state=64, shuffle=True)
        # 构建dataset
        train_dataset = TensorDataset(torch.from_numpy(x_train.values), torch.from_numpy(y_train.values))
        valid_dataset = TensorDataset(torch.from_numpy(x_valid.values), torch.from_numpy(y_valid.values))
        # 构建dataloader
        train_dataloader = DataLoader(train_dataset, shuffle=True, batch_size=8, drop_last=False)
        valid_dataloader = DataLoader(valid_dataset, shuffle=True, batch_size=8, drop_last=False)
        return train_dataloader, valid_dataloader, valid_dataset
    except FileNotFoundError:
        logger.error(f"文件 {file_path} 不存在")
        return None, None, None
    except pd.errors.EmptyDataError:
        logger.error(f"文件 {file_path} 为空")
        return None, None, None
    except pd.errors.ParserError:
        logger.error(f"解析文件 {file_path} 时出错")
        return None, None, None
    except Exception as e:
        logger.error(f"创建数据集时发生错误，错误信息：{e}")
        return None, None, None


def train(train_dataloader):
    """模型训练"""
    # 初始化模型
    model = PhonePriceModel().to(param.device)
    # 初始化损失函数
    criterion = nn.CrossEntropyLoss()
    # 初始化优化器
    optimizer = optim.Adam(model.parameters(), lr=param.lr)
    # 初始化训练轮次
    epoch = param.epoch
    model.train()
    # 初始化学习率调整器
    # scheduler = StepLR(optimizer, step_size=30, gamma=0.1)
    # 初始化开始时间
    start_time_all = time.time()
    time_epoch_10 = 0
    # 两个遍历，开始模型训练
    try:
        # logger.success("模型及数据加载成功，开始训练...")
        for epoch_index in range(epoch):

            # 开始一个轮次，初始化开始时间，损失值
            start_time = time.time()
            total_loss = 0
            for x, y in train_dataloader:
                x, y = x.to(param.device), y.to(param.device)
                output = model(x)  # 前向传播
                loss = criterion(output, y)  # 计算损失值
                if torch.isnan(loss):
                    logger.error("损失值为Nan,可能存在数值不稳定问题，请检查！")
                    raise ValueError("损失值为Nan，训练无法继续")
                optimizer.zero_grad()  # 梯度归零
                loss.backward()  # 反向传播
                optimizer.step()  # 参数更新
                total_loss += loss.item()

            # 一个轮次训练完成，输出结果
            end_time = time.time()
            time_epoch_10 += (end_time - start_time)
            if (epoch_index + 1) % 10 == 0:
                # scheduler.step()
                logger.info(f"当前Epoch:{epoch_index + 1}, 当前总loss:{total_loss:.2f}, 该批10轮次用时：{time_epoch_10:.2f}秒")
                time_epoch_10 = 0
    except Exception as e:
        logger.error(f"模型训练时发生错误，错误信息：{e}")
    # 所有轮次训练完成，保存模型
    try:
        os.makedirs(os.path.dirname(param.save_model), exist_ok=True)
        torch.save(model.state_dict(), param.save_model)
        logger.success(f"模型保存成功！")
    except Exception as e:
        logger.error(f"保存模型错误|，错误信息：{e}")
    finally:
        logger.info(f"训练完成，共耗时：{(time.time() - start_time_all):.2f}秒")


def evaluation(valid_dataloader, valid_dataset):
    # 加载模型及训练好的参数
    model = PhonePriceModel()
    model.load_state_dict(torch.load(param.save_model))
    # 初始化数据
    correct = 0
    model.eval()
    # 遍历dataloader开始验证
    with torch.no_grad():
        try:
            for x, y in valid_dataloader:
                output = model(x)
                y_pred = torch.argmax(output, dim=1)  # 找索引
                correct += (y_pred == y).sum()
            # 获取预测精度
            acc = correct.item() / len(valid_dataset)
            logger.success(f"模型评估结束，准确率：{acc}")
        except Exception as e:
            logger.error(f"模型评估时发生错误，错误信息：{e}")


if __name__ == '__main__':
    param = ParametersConfig()
    file = param.phone_price_data
    # 获取数据集
    train_dataloader, valid_dataloader, valid_dataset = data_preprocess(file)
    if train_dataloader:
        logger.success(f"数据加载成功，准备开始模型训练...")
        train(train_dataloader)
        logger.info("开始模型评估...")
        evaluation(valid_dataloader, valid_dataset)
