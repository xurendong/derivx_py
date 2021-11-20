
# -*- coding: utf-8 -*-

# Copyright (c) 2021-2021 the DerivX authors
# All rights reserved.
#
# The project sponsor and lead author is Xu Rendong.
# E-mail: xrd@ustc.edu, QQ: 277195007, WeChat: ustc_xrd
# See the contributors file for names of other contributors.
#
# Commercial use of this code in source and binary forms is
# governed by a LGPL v3 license. You may get a copy from the
# root directory. Or else you should get a specific written 
# permission from the project author.
#
# Individual and educational use of this code in source and
# binary forms is governed by a 3-clause BSD license. You may
# get a copy from the root directory. Certainly welcome you
# to contribute code of all sorts.
#
# Be sure to retain the above copyright notice and conditions.

import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(suppress = True) # 不以科学计数法输出
np.set_printoptions(threshold = np.inf) # 指定超过多少使用省略号，np.inf 为无限大

def ShowPlot_Frequency(price, title, xlabel):
    n, bins, patches = plt.hist(price[:, -1], bins = 50, normed = True, facecolor = "blue", alpha = 0.75)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Frequency")
    plt.grid(True, alpha = 0.5)
    plt.show()

def ShowPlot_Distribution(price, path, step, title, ylabel):
    plt.figure()
    ax = plt.subplot2grid((1, 1), (0, 0), colspan = 1, rowspan = 1)
    ax.set_xlabel("Steps")
    ax.set_ylabel(ylabel)
    for i in range(path):
        ax.plot(range(step), price[i, :], color = np.random.rand(3), ls = "-", lw = 1.0)
    #ax.legend(loc = "best") # 不显示图例
    ax.margins(0, 0) # 0 ~ 1
    ax.set_title(title)
    plt.subplots_adjust(left = 0.05, bottom = 0.05, right = 0.99, top = 0.98, wspace = 0.0, hspace = 0.0)
    plt.grid(True, alpha = 0.5)
    plt.show()

# 几何布朗运动 (指数布朗运动) Geometric Brownian Motion
# 被Black-Scholes（1973）引入到期权定价文献中，虽然这个过程有一些缺陷，并且与实证研究存在着冲突，但是仍然是一种期权和衍生品估值过程的基础过程。
def SP_GBM():
    s = 1.0 # 初始价格
    r = 0.03 # 无风险利率，期望收益率
    v = 0.24 # 收益率波动率
    t = 1.0 # 时间长度
    year_days = 252 # 年交易日数
    dt = t / year_days # 步长时间
    step = int(year_days * t) + 1
    path = 10000 # 路径数量
    
    price = np.zeros((path, step))
    price[:, 0] = s
    for i in range(1, step):
        price[:, i] = price[:, i - 1] * np.exp((r - 0.5 * v ** 2) * dt + v * np.sqrt(dt) * np.random.standard_normal(path))
    
    ShowPlot_Frequency(price, "Final-Price-Frequency", "Final-Price")
    ShowPlot_Distribution(price, 1000, step, "Price - Steps", "Price")

# CIR模型 (平方根扩散过程) Cox–Ingersoll–Ross model (Square-Root Diffusion)
# 由Cox、Ingersoll和Ross（1985）所提出，用于对均值回复的数量，例如利率或波动率进行建模，除了均值回复的特性以外，这个过程总是保持为正数。
def SP_CIR():
    s = 0.05 # 初始利息率
    kappa = 3.0 # 均值回归系数
    theta = 0.02 # 长期均值项
    sigma = 0.1 # 利息率波动率
    t = 2.0 # 时间长度
    year_days = 252 # 年交易日数
    dt = t / year_days # 步长时间
    step = int(year_days * t) + 1
    path = 10000 # 路径数量
    
    price = np.zeros((path, step))
    price[:, 0] = s
    for i in range(1, step):
        d_price = kappa * (theta - np.maximum(price[:, i - 1], 0.0)) * dt + sigma * np.sqrt(np.maximum(price[:, i - 1], 0.0)) * np.sqrt(dt) * np.random.standard_normal(path)
        price[:, i] = price[:, i - 1] + d_price
    price = np.maximum(price, 0.0)
    
    ShowPlot_Frequency(price, "Final-Interest-Frequency", "Final-Interest")
    ShowPlot_Distribution(price, 1000, step, "Interest - Steps", "Interest")

# 跳跃扩散过程 Jump Diffusion Process
# 由Merton（1976）所给出，为几何布朗运动增加了对数正态分布的条约成分，这允许我们考虑，例如，短期虚值（OTM）的期权通常需要在较大条约的可能性下定价。
def SP_JDP():
    s = 1.0 # 初始价格
    r = 0.05 # 收益率均值，漂移率
    v = 0.24 # 收益率波动率
    lamb = 0.75 # 跳跃强度
    mu = 0.6 # 预期跳跃均值，正负决定跳跃方向，需要改进
    delta = 0.25 # 跳跃强度标准差
    t = 1.0 # 时间长度
    year_days = 252 # 年交易日数
    dt = t / year_days # 步长时间
    step = int(year_days * t) + 1
    path = 10000 # 路径数量
    
    price = np.zeros((path, step))
    price[:, 0] = s
    kappa = lamb * (np.exp(mu + 0.5 * delta ** 2) - 1.0)
    sn1 = np.random.standard_normal((path, step))
    sn2 = np.random.standard_normal((path, step))
    poi = np.random.poisson(lamb * dt, (path, step))
    for i in range(1, step):
        price[:, i] = price[:, i - 1] * (np.exp((r - kappa - 0.5 * v ** 2) * dt) + v * np.sqrt(dt) * sn1[:, i] + (np.exp(mu + delta * sn2[:, i]) - 1.0) * poi[:, i])
        price[:, i] = np.maximum(price[:, i], 0.0)
    
    ShowPlot_Frequency(price, "Final-Price-Frequency", "Final-Price")
    ShowPlot_Distribution(price, 1000, step, "Price - Steps", "Price")

# Heston模型 (随机波动率模型) Heston Model (Stochastic Volatility Model)
# 由Steven Heston（1993）提出的描述标的资产波动率变化的数学模型，这种模型假设资产收益率的波动率并不恒定，也不确定，而是跟随一个随机过程来运动。
def SP_HEST():
    s = 1.0 # 初始价格
    r = 0.03 # 收益率均值，漂移率
    v = 0.1 # 初始波动率
    kappa = 3.0 # 波动率均值回归速度
    theta = 0.25 # 波动率长期均值项
    sigma = 0.1 # 波动率的波动率
    rho = 0.6 # 两个随机过程的相关系数
    t = 1.0 # 时间长度
    year_days = 252 # 年交易日数
    dt = t / year_days # 步长时间
    step = int(year_days * t) + 1
    path = 10000 # 路径数量
    
    #corr_mat = np.zeros((2, 2))
    #corr_mat[0, :] = [1.0, rho]
    #corr_mat[1, :] = [rho, 1.0]
    corr_mat = [[1.0, rho], [rho, 1.0]]
    chol_mat = np.linalg.cholesky(corr_mat) # 两个随机过程的相关系数的 Cholesky 分解
    rand_mat = np.random.standard_normal((2, path, step)) # 这里也可以用对偶采样法减少数据生成量
    
    vol = np.zeros((path, step))
    vol[:, 0] = v
    for i in range(1, step):
        rand = np.dot(chol_mat, rand_mat[:, :, i]) # 也可以用：chol_mat @ rand_mat[:, :, i]
        d_vol = kappa * (theta - np.maximum(vol[:, i - 1], 0.0)) * dt + sigma * np.sqrt(np.maximum(vol[:, i - 1], 0.0)) * np.sqrt(dt) * rand[1]
        vol[:, i] = vol[:, i - 1] + d_vol
    vol = np.maximum(vol, 0.0)
    
    ShowPlot_Frequency(vol, "Final-vol-Frequency", "Final-vol")
    ShowPlot_Distribution(vol, 1000, step, "vol - Steps", "vol")
    
    price = np.zeros((path, step))
    price[:, 0] = s
    for i in range(1, step):
        rand = np.dot(chol_mat, rand_mat[:, :, i]) # 也可以用：chol_mat @ rand_mat[:, :, i]
        price[:, i] = price[:, i - 1] * np.exp((r - 0.5 * vol[:, i]) * dt + np.sqrt(vol[:, i]) * rand[0] * np.sqrt(dt))
    
    ShowPlot_Frequency(price, "Final-Price-Frequency", "Final-Price")
    ShowPlot_Distribution(price, 1000, step, "Price - Steps", "Price")

# SABR模型 Stochastic Alpha Beta Rho
# 由Hagan（2002）提出的一种随机波动率模型，在抛弃了原始的BSM模型中对于波动率为某一常数的假定，假设隐含波动率同样是符合几何布朗运动的，
# 并且将隐含波动率设定为标的价格和合约行权价的函数，结合了隐含波动率修正模型的两种思路（随机波动率模型和局部波动率模型），更为准确的动态刻画出吻合市场特征的隐含波动率曲线。
def SP_SABR():
    s = 0.06 # 初始远期利率
    v = 0.2 # 初始波动率
    beta = 0.5 # 远期利率分布的力度
    rho = 0.6 # 两个随机过程的相关系数
    sigma = 0.2 # 波动率的波动率
    t = 1.0 # 时间长度
    year_days = 252 # 年交易日数
    dt = t / year_days # 步长时间
    step = int(year_days * t) + 1
    path = 10000 # 路径数量
    
    #corr_mat = np.zeros((2, 2))
    #corr_mat[0, :] = [1.0, rho]
    #corr_mat[1, :] = [rho, 1.0]
    corr_mat = [[1.0, rho], [rho, 1.0]]
    chol_mat = np.linalg.cholesky(corr_mat) # 两个相关随机过程的 Cholesky 分解
    rand_mat = np.random.standard_normal((2, path, step)) # 这里也可以用对偶采样法减少数据生成量
    
    vol = np.zeros((path, step))
    vol[:, 0] = v
    for i in range(1, step):
        rand = np.dot(chol_mat, rand_mat[:, :, i]) # 也可以用：chol_mat @ rand_mat[:, :, i]
        d_vol = sigma * np.maximum(vol[:, i - 1], 0.0) * np.sqrt(dt) * rand[1]
        vol[:, i] = vol[:, i - 1] + d_vol
    vol = np.maximum(vol, 0.0)
    
    ShowPlot_Frequency(vol, "Final-vol-Frequency", "Final-vol")
    ShowPlot_Distribution(vol, 1000, step, "vol - Steps", "vol")
    
    price = np.zeros((path, step))
    price[:, 0] = s
    for i in range(1, step):
        rand = np.dot(chol_mat, rand_mat[:, :, i]) # 也可以用：chol_mat @ rand_mat[:, :, i]
        d_price = vol[:, i - 1] * np.power(np.maximum(price[:, i - 1], 0.0), beta) * np.sqrt(dt) * rand[0] # price 会有小于零的异常值出现的，故增加 np.maximum 判断
        price[:, i] = price[:, i - 1] + d_price
    
    ShowPlot_Frequency(price, "Final-Price-Frequency", "Final-Price")
    ShowPlot_Distribution(price, 1000, step, "Price - Steps", "Price")

if __name__ == "__main__":
    #SP_GBM()
    #SP_CIR()
    #SP_JDP()
    #SP_HEST()
    SP_SABR()
