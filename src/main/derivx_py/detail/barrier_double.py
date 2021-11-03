
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
        self.s = 0.0 # 标的价格
        self.h = 0.0 # 障碍价格
        self.k = 0.0 # 行权价格
        self.x = 0.0 # 未触及障碍所需支付资金
        self.v = 0.0 # 波动率
        self.r = 0.0 # 无风险利率
        self.q = 0.0 # 年化分红率
        self.t = 0.0 # 年化到期期限
        self.p = 0.0 # 参与率，未敲出情况下客户对收益的占比要求
        self.is_call = True # 看涨看跌
        self.is_knock = False # 是否已经敲入敲出
        self.is_kop_delay = False # 敲出后是立即还是延期支付资金
        self.barrier_type = 0 # 障碍类型
        
        self.error_message = ""

    def GetError(self):
        return self.error_message

    def InitArgs(self, config): # config：dict
        try:
            self.s = config["s"]
            self.h = config["h"]
            self.k = config["k"]
            self.x = config["x"]
            self.v = config["v"]
            self.r = config["r"]
            self.q = config["q"]
            self.t = config["t"]
            self.p = config["p"]
            self.is_call = config["is_call"]
            self.is_knock = config["is_knock"]
            self.is_kop_delay = config["is_kop_delay"]
            self.barrier_type = config["barrier_type"]
            return 0
        except Exception as e:
            self.error_message = "参数设置发生异常！%s" % e
        return -1
