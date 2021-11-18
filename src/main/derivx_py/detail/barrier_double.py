
# -*- coding: utf-8 -*-

# Copyright (c) 2021-2021 the DerivX authors
# All rights reserved.
#
# The project sponsor and lead author is Xu Rendong.
# E-mail: xrd@ustc.edu, QQ: 277195007, WeChat: xrd_ustc
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

import utility

class Barrier_Double(object):
    def __init__(self):
        self.rand_rows = 0 # 随机数据行数 # InitRand
        self.rand_cols = 0 # 随机数据列数 # InitRand
        self.rand_seed = np.array([]) # 随机数据种子 # InitRand # 非负整数，有效位数不超逻辑处理器数量
        
        self.dual_smooth = True # 对偶平滑路径 # InitPath
        self.runs_size = 0 # 模拟路径数量 # InitPath
        self.runs_step = 0 # 价格变动步数 # InitPath
        self.year_days = 0 # 年交易日数量 # InitPath
        self.sigma = 0.0 # 波动率 # InitPath
        self.risk_free_rate = 0.0 # 无风险利率 # InitPath
        self.basis_rate = 0.0 # 股息或贴水 # InitPath
        self.price_limit_ratio = 0.0 # 涨跌停限制幅度 # InitPath
        self.price_limit_style = 0 # 涨跌停限制方式，0 不限制，1 超限部分移至下日，2 超限部分直接削掉 # InitPath
        
        self.s = 0.0 # 标的价格
        self.h_l = 0.0 # 障碍价格，低
        self.h_h = 0.0 # 障碍价格，高
        self.k_l = 0.0 # 行权价格，低
        self.k_h = 0.0 # 行权价格，高
        self.x = 0.0 # 敲出后需支付的资金
        self.v = 0.0 # 波动率 # 双鲨未用
        self.r = 0.0 # 无风险利率 # 双鲨未用
        self.q = 0.0 # 年化分红率 # 双鲨未用
        self.t = 0.0 # 年化到期期限 # 双鲨未用
        self.p = 0.0 # 参与率，未敲出情况下客户对收益的占比要求
        self.is_kop_delay = False # 敲出后是立即还是延期支付资金
        self.barrier_type = 0 # 障碍类型
        
        self.error_message = ""

    def GetError(self):
        return self.error_message

    def InitArgs(self, config): # config：dict
        try:
            self.rand_rows = config["rand_rows"]
            self.rand_cols = config["rand_cols"]
            self.rand_seed = config["rand_seed"].copy() # copy
            self.dual_smooth = config["dual_smooth"]
            self.runs_size = config["runs_size"]
            self.runs_step = config["runs_step"]
            self.year_days = config["year_days"]
            self.sigma = config["sigma"]
            self.risk_free_rate = config["risk_free_rate"]
            self.basis_rate = config["basis_rate"]
            self.price_limit_ratio = config["price_limit_ratio"]
            self.price_limit_style = config["price_limit_style"]
            self.s = config["s"]
            self.h_l = config["h_l"]
            self.h_h = config["h_h"]
            self.k_l = config["k_l"]
            self.k_h = config["k_h"]
            self.x = config["x"]
            self.v = config["v"]
            self.r = config["r"]
            self.q = config["q"]
            self.t = config["t"]
            self.p = config["p"]
            self.is_kop_delay = config["is_kop_delay"]
            self.barrier_type = config["barrier_type"]
            return 0
        except Exception as e:
            self.error_message = "参数设置发生异常！%s" % e
        return -1
