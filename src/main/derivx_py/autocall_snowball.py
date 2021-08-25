
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

import utility

class Autocall_Snowball(object):
    def __init__(self):
        self.rand_rows = 0 # 随机数据行数 # InitRand
        self.rand_cols = 0 # 随机数据列数 # InitRand
        self.rand_seed = np.array([]) # 随机数据种子 # InitRand // 非负整数，有效位数不超逻辑处理器数量
        
        self.dual_smooth = True # 对偶平滑路径 # InitPath
        self.runs_size = 0 # 模拟路径数量 # InitPath
        self.runs_step = 0 # 价格变动步数 # InitPath
        self.year_days = 0 # 年交易日数量 # InitPath
        self.sigma = 0.0 # 波动率 # InitPath
        self.risk_free_rate = 0.0 # 无风险利率 # InitPath
        self.basis_rate = 0.0 # 股息或贴水 # InitPath
        self.price_limit_ratio = 0.0 # 涨跌停限制幅度 # InitPath
        self.price_limit_style = 0 # 涨跌停限制方式，0 不限制，1 超限部分移至下日，2 超限部分直接削掉 // InitPath
        
        self.notional = 0.0 # 名义本金
        self.trade_long = True # 交易方向
        self.start_price = 0.0 # 初始价格
        self.strike_price = 0.0 # 敲入后执行价格
        self.knock_o_ratio = 0.0 # 敲出比率，非百分比
        self.knock_i_ratio = 0.0 # 敲入比率，非百分比
        self.knock_o_steps = 0.0 # 敲出比例逐月递减率
        self.knock_i_valid = True # 是否有下方敲入障碍
        self.knock_i_occur = False # 是否已经发生敲入
        self.knock_i_margin_call = True # 是否敲入后可追加保证金
        self.coupon_rate = 0.0 # 客户年化收益率
        self.margin_rate = 0.0 # 保证金比例
        self.margin_interest = 0.0 # 保证金利率
        self.prefix_coupon = 0.0 # 不管敲入敲出和到期时间，客户都要求得到固定收益，相当于前端扣费的意思
        self.prefix_coupon_ann = False # False 为绝对收益率，True 为年化收益率
        self.prefix_coupon_use = False # 是否支付 prefix 收益
        self.ukiuko_coupon = 0.0 # 对于无敲出无敲入的情况，客户只要求得到固定收益
        self.ukiuko_coupon_ann = False # False 为绝对收益率，True 为年化收益率
        self.ukiuko_coupon_use = False # 是否支付 ukiuko 收益
        self.calc_price = np.array([]) # 计算价格序列
        self.run_from = 0 # 起始天数，第一天为零
        self.run_days = 0 # 运行天数
        self.knock_o_days = np.array([]) # 敲出日期序列
        self.knock_o_rate = np.array([]) # 敲出比率序列
        
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
            self.notional = config["notional"]
            self.trade_long = config["trade_long"]
            self.start_price = config["start_price"]
            self.strike_price = config["strike_price"]
            self.knock_o_ratio = config["knock_o_ratio"]
            self.knock_i_ratio = config["knock_i_ratio"]
            self.knock_o_steps = config["knock_o_steps"]
            self.knock_i_valid = config["knock_i_valid"]
            self.knock_i_occur = config["knock_i_occur"]
            self.knock_i_margin_call = config["knock_i_margin_call"]
            self.coupon_rate = config["coupon_rate"]
            self.margin_rate = config["margin_rate"]
            self.margin_interest = config["margin_interest"]
            self.prefix_coupon = config["prefix_coupon"]
            self.prefix_coupon_ann = config["prefix_coupon_ann"]
            self.prefix_coupon_use = config["prefix_coupon_use"]
            self.ukiuko_coupon = config["ukiuko_coupon"]
            self.ukiuko_coupon_ann = config["ukiuko_coupon_ann"]
            self.ukiuko_coupon_use = config["ukiuko_coupon_use"]
            self.calc_price = config["calc_price"].copy() # copy
            self.run_from = config["run_from"]
            self.run_days = config["run_days"]
            self.knock_o_days = config["knock_o_days"].copy() # copy
            self.knock_o_rate = config["knock_o_rate"].copy() # copy
            return 0
        except Exception as e:
            self.error_message = "参数设置发生异常！%s" % e
        return -1