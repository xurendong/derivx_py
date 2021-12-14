
# -*- coding: utf-8 -*-

# Copyright (c) 2021-2022 the DerivX authors
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

import utility

class Digital_Gap(object):
    def __init__(self):
        self.s = 0.0 # 标的价格
        self.k_1 = 0.0 # 行权价格
        self.k_2 = 0.0 # 行权价格
        self.r = 0.0 # 无风险利率
        self.q = 0.0 # 年化分红率
        self.v = 0.0 # 波动率
        self.t = 0.0 # 年化到期期限
        self.is_call = True # 看涨看跌
        
        self.error_message = ""

    def GetError(self):
        return self.error_message

    def InitArgs(self, config): # config：dict
        try:
            self.s = config["s"]
            self.k_1 = config["k_1"]
            self.k_2 = config["k_2"]
            self.r = config["r"]
            self.q = config["q"]
            self.v = config["v"]
            self.t = config["t"]
            self.is_call = config["is_call"]
            return 0
        except Exception as e:
            self.error_message = "参数设置发生异常！%s" % e
        return -1

class Digital_CashOrNothing(object):
    def __init__(self):
        self.s = 0.0 # 标的价格
        self.k = 0.0 # 行权价格
        self.r = 0.0 # 无风险利率
        self.q = 0.0 # 年化分红率
        self.v = 0.0 # 波动率
        self.t = 0.0 # 年化到期期限
        self.cash = 0.0 # 现金回报
        self.is_call = True # 看涨看跌
        
        self.error_message = ""

    def GetError(self):
        return self.error_message

    def InitArgs(self, config): # config：dict
        try:
            self.s = config["s"]
            self.k = config["k"]
            self.r = config["r"]
            self.q = config["q"]
            self.v = config["v"]
            self.t = config["t"]
            self.cash = config["cash"]
            self.is_call = config["is_call"]
            return 0
        except Exception as e:
            self.error_message = "参数设置发生异常！%s" % e
        return -1

class Digital_AssetOrNothing(object):
    def __init__(self):
        self.s = 0.0 # 标的价格
        self.k = 0.0 # 行权价格
        self.r = 0.0 # 无风险利率
        self.q = 0.0 # 年化分红率
        self.v = 0.0 # 波动率
        self.t = 0.0 # 年化到期期限
        self.is_call = True # 看涨看跌
        
        self.error_message = ""

    def GetError(self):
        return self.error_message

    def InitArgs(self, config): # config：dict
        try:
            self.s = config["s"]
            self.k = config["k"]
            self.r = config["r"]
            self.q = config["q"]
            self.v = config["v"]
            self.t = config["t"]
            self.is_call = config["is_call"]
            return 0
        except Exception as e:
            self.error_message = "参数设置发生异常！%s" % e
        return -1

class Digital_SuperShare(object):
    def __init__(self):
        self.s = 0.0 # 标的价格
        self.k_l = 0.0 # 低端行权价格
        self.k_h = 0.0 # 高端行权价格
        self.r = 0.0 # 无风险利率
        self.q = 0.0 # 年化分红率
        self.v = 0.0 # 波动率
        self.t = 0.0 # 年化到期期限
        
        self.error_message = ""

    def GetError(self):
        return self.error_message

    def InitArgs(self, config): # config：dict
        try:
            self.s = config["s"]
            self.k_l = config["k_l"]
            self.k_h = config["k_h"]
            self.r = config["r"]
            self.q = config["q"]
            self.v = config["v"]
            self.t = config["t"]
            return 0
        except Exception as e:
            self.error_message = "参数设置发生异常！%s" % e
        return -1
