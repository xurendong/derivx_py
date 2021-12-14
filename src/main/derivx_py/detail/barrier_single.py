
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

import numpy as np
from scipy import stats

import utility

def sb_x1(s, k, v, u, t): # k v t != 0
    return np.log(s / k) / (v * t ** 0.5) + (1.0 + u) * v * t ** 0.5

def sb_x2(s, h, v, u, t): # h v t != 0
    return np.log(s / h) / (v * t ** 0.5) + (1.0 + u) * v * t ** 0.5

def sb_y1(s, h, k, v, u, t): # s k v t != 0
    return np.log(h ** 2 / (s * k)) / (v * t ** 0.5) + (1.0 + u) * v * t ** 0.5

def sb_y2(s, h, v, u, t): # s v t != 0
    return np.log(h / s) / (v * t ** 0.5) + (1.0 + u) * v * t ** 0.5

def sb_z(s, h, v, n, t): # s v t != 0
    return np.log(h / s) / (v * t ** 0.5) + n * v * t ** 0.5

def sb_u(r, q, v): # v != 0
    return (r - q) / v ** 2 - 0.5 # (r - q - 0.5 * v ** 2) / v ** 2

def sb_n(r, v, u): # v != 0
    return (u ** 2 + 2.0 * r / v ** 2) ** 0.5

def sb_A(phi, s, k, v, r, q, t): # k v t != 0
    u = sb_u(r, q, v)
    x1 = sb_x1(s, k, v, u, t)
    return phi * s * np.exp(-q * t) * stats.norm.cdf(phi * x1) - phi * k * np.exp(-r * t) * stats.norm.cdf(phi * (x1 - v * t ** 0.5))

def sb_B(phi, s, h, k, v, r, q, t): # h v t != 0
    u = sb_u(r, q, v)
    x2 = sb_x2(s, h, v, u, t)
    return phi * s * np.exp(-q * t) * stats.norm.cdf(phi * x2) - phi * k * np.exp(-r * t) * stats.norm.cdf(phi * (x2 - v * t ** 0.5))

def sb_C(phi, eta, s, h, k, v, r, q, t): # s k v t != 0
    u = sb_u(r, q, v)
    y1 = sb_y1(s, h, k, v, u, t)
    return phi * s * np.exp(-q * t) * (h / s) ** (2.0 * (u + 1.0)) * stats.norm.cdf(eta * y1) - phi * k * np.exp(-r * t) * (h / s) ** (2.0 * u) * stats.norm.cdf(eta * (y1 - v * t ** 0.5))

def sb_D(phi, eta, s, h, k, v, r, q, t): # s v t != 0
    u = sb_u(r, q, v)
    y2 = sb_y2(s, h, v, u, t)
    return phi * s * np.exp(-q * t) * (h / s) ** (2.0 * (u + 1.0)) * stats.norm.cdf(eta * y2) - phi * k * np.exp(-r * t) * (h / s) ** (2.0 * u) * stats.norm.cdf(eta * (y2 - v * t ** 0.5))

def sb_E(eta, x, s, h, v, r, q, t): # s h v t != 0
    u = sb_u(r, q, v)
    x2 = sb_x2(s, h, v, u, t)
    y2 = sb_y2(s, h, v, u, t)
    return x * np.exp(-r * t) * (stats.norm.cdf(eta * (x2 - v * t ** 0.5)) - (h / s) ** (2.0 * u) * stats.norm.cdf(eta * (y2 - v * t ** 0.5)))

def sb_F(eta, x, s, h, v, r, q, t, is_kop_delay): # s v t != 0
    u = sb_u(r, q, v)
    n = sb_n(r, v, u) # 立即支付
    if is_kop_delay == True: # 延迟支付
        n = (r ** 2 + v ** 4 / 4.0 + r * v ** 2) ** 0.5 / v ** 2
    z = sb_z(s, h, v, n, t)
    return x * ((h / s) ** (u + n) * stats.norm.cdf(eta * z) + (h / s) ** (u - n) * stats.norm.cdf(eta * (z - 2.0 * n * v * t ** 0.5)))

class Config(object):
    def __init__(self, s, h, k, x, v, r, q, t, p, is_call, is_knock, is_kop_delay, barrier_type):
        self.s = s # 标的价格
        self.h = h # 障碍价格
        self.k = k # 行权价格
        self.x = x # 未触及障碍所需支付资金
        self.v = v # 波动率
        self.r = r # 无风险利率
        self.q = q # 年化分红率
        self.t = t # 年化到期期限
        self.p = p # 参与率，未敲出情况下客户对收益的占比要求
        self.is_call = is_call # 看涨看跌
        self.is_kop_delay = is_kop_delay # 敲出后是立即还是延期支付资金
        self.barrier_type = barrier_type # 障碍类型

    def ToArgs(self):
        return self.__dict__

class Barrier_Single(object):
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
        self.is_kop_delay = False # 敲出后是立即还是延期支付资金
        self.barrier_type = 0 # 障碍类型
        
        self.up_in    = 1 # 向上敲入
        self.down_in  = 2 # 向下敲入
        self.up_out   = 3 # 向上敲出
        self.down_out = 4 # 向下敲出
        
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
            self.is_kop_delay = config["is_kop_delay"]
            self.barrier_type = config["barrier_type"]
            return 0
        except Exception as e:
            self.error_message = "参数设置发生异常！%s" % e
        return -1

    def CalcPrice(self):
        result = 0.0
        if self.barrier_type == self.up_in:
            if self.is_call == True: # 看涨认购
                eta = -1.0
                phi = 1.0
                # k == h 时下面两组 result 相同
                if self.k >= self.h:
                    A = sb_A(phi, self.s, self.k, self.v, self.r, self.q, self.t)
                    E = sb_E(eta, self.x, self.s, self.h, self.v, self.r, self.q, self.t)
                    result = self.p * A + E
                if self.k < self.h:
                    B = sb_B(phi, self.s, self.h, self.k, self.v, self.r, self.q, self.t)
                    C = sb_C(phi, eta, self.s, self.h, self.k, self.v, self.r, self.q, self.t)
                    D = sb_D(phi, eta, self.s, self.h, self.k, self.v, self.r, self.q, self.t)
                    E = sb_E(eta, self.x, self.s, self.h, self.v, self.r, self.q, self.t)
                    result = self.p * (B - C + D) + E
            else: # 看跌认沽
                eta = -1.0
                phi = -1.0
                # k == h 时下面两组 result 相同
                if self.k >= self.h:
                    A = sb_A(phi, self.s, self.k, self.v, self.r, self.q, self.t)
                    B = sb_B(phi, self.s, self.h, self.k, self.v, self.r, self.q, self.t)
                    D = sb_D(phi, eta, self.s, self.h, self.k, self.v, self.r, self.q, self.t)
                    E = sb_E(eta, self.x, self.s, self.h, self.v, self.r, self.q, self.t)
                    result = self.p * (A - B + D) + E
                if self.k < self.h:
                    C = sb_C(phi, eta, self.s, self.h, self.k, self.v, self.r, self.q, self.t)
                    E = sb_E(eta, self.x, self.s, self.h, self.v, self.r, self.q, self.t)
                    result = self.p * C + E
        elif self.barrier_type == self.down_in:
            if self.is_call == True: # 看涨认购
                eta = 1.0
                phi = 1.0
                # k == h 时下面两组 result 相同
                if self.k >= self.h:
                    C = sb_C(phi, eta, self.s, self.h, self.k, self.v, self.r, self.q, self.t)
                    E = sb_E(eta, self.x, self.s, self.h, self.v, self.r, self.q, self.t)
                    result = self.p * C + E
                if self.k < self.h:
                    A = sb_A(phi, self.s, self.k, self.v, self.r, self.q, self.t)
                    B = sb_B(phi, self.s, self.h, self.k, self.v, self.r, self.q, self.t)
                    D = sb_D(phi, eta, self.s, self.h, self.k, self.v, self.r, self.q, self.t)
                    E = sb_E(eta, self.x, self.s, self.h, self.v, self.r, self.q, self.t)
                    result = self.p * (A - B + D) + E
            else: # 看跌认沽
                eta = 1.0
                phi = -1.0
                # k == h 时下面两组 result 相同
                if self.k >= self.h:
                    B = sb_B(phi, self.s, self.h, self.k, self.v, self.r, self.q, self.t)
                    C = sb_C(phi, eta, self.s, self.h, self.k, self.v, self.r, self.q, self.t)
                    D = sb_D(phi, eta, self.s, self.h, self.k, self.v, self.r, self.q, self.t)
                    E = sb_E(eta, self.x, self.s, self.h, self.v, self.r, self.q, self.t)
                    result = self.p * (B - C + D) + E
                if self.k < self.h:
                    A = sb_A(phi, self.s, self.k, self.v, self.r, self.q, self.t)
                    E = sb_E(eta, self.x, self.s, self.h, self.v, self.r, self.q, self.t)
                    result = self.p * A + E
        elif self.barrier_type == self.up_out:
            if self.is_call == True: # 看涨认购
                eta = -1.0
                phi = 1.0
                # k == h 时下面两组 result 相同
                if self.k >= self.h:
                    F = sb_F(eta, self.x, self.s, self.h, self.v, self.r, self.q, self.t, self.is_kop_delay)
                    result = F # self.p * 0.0 + F
                if self.k < self.h:
                    A = sb_A(phi, self.s, self.k, self.v, self.r, self.q, self.t)
                    B = sb_B(phi, self.s, self.h, self.k, self.v, self.r, self.q, self.t)
                    C = sb_C(phi, eta, self.s, self.h, self.k, self.v, self.r, self.q, self.t)
                    D = sb_D(phi, eta, self.s, self.h, self.k, self.v, self.r, self.q, self.t)
                    F = sb_F(eta, self.x, self.s, self.h, self.v, self.r, self.q, self.t, self.is_kop_delay)
                    result = self.p * (A - B + C - D) + F
            else: # 看跌认沽
                eta = -1.0
                phi = -1.0
                # k == h 时下面两组 result 相同
                if self.k >= self.h:
                    B = sb_B(phi, self.s, self.h, self.k, self.v, self.r, self.q, self.t)
                    D = sb_D(phi, eta, self.s, self.h, self.k, self.v, self.r, self.q, self.t)
                    F = sb_F(eta, self.x, self.s, self.h, self.v, self.r, self.q, self.t, self.is_kop_delay)
                    result = self.p * (B - D) + F
                if self.k < self.h:
                    A = sb_A(phi, self.s, self.k, self.v, self.r, self.q, self.t)
                    C = sb_C(phi, eta, self.s, self.h, self.k, self.v, self.r, self.q, self.t)
                    F = sb_F(eta, self.x, self.s, self.h, self.v, self.r, self.q, self.t, self.is_kop_delay)
                    result = self.p * (A - C) + F
        elif self.barrier_type == self.down_out:
            if self.is_call == True: # 看涨认购
                eta = 1.0
                phi = 1.0
                # k == h 时下面两组 result 相同
                if self.k >= self.h:
                    A = sb_A(phi, self.s, self.k, self.v, self.r, self.q, self.t)
                    C = sb_C(phi, eta, self.s, self.h, self.k, self.v, self.r, self.q, self.t)
                    F = sb_F(eta, self.x, self.s, self.h, self.v, self.r, self.q, self.t, self.is_kop_delay)
                    result = self.p * (A - C) + F
                if self.k < self.h:
                    B = sb_B(phi, self.s, self.h, self.k, self.v, self.r, self.q, self.t)
                    D = sb_D(phi, eta, self.s, self.h, self.k, self.v, self.r, self.q, self.t)
                    F = sb_F(eta, self.x, self.s, self.h, self.v, self.r, self.q, self.t, self.is_kop_delay)
                    result = self.p * (B - D) + F
            else: # 看跌认沽
                eta = 1.0
                phi = -1.0
                # k == h 时下面两组 result 相同
                if self.k >= self.h:
                    A = sb_A(phi, self.s, self.k, self.v, self.r, self.q, self.t)
                    B = sb_B(phi, self.s, self.h, self.k, self.v, self.r, self.q, self.t)
                    C = sb_C(phi, eta, self.s, self.h, self.k, self.v, self.r, self.q, self.t)
                    D = sb_D(phi, eta, self.s, self.h, self.k, self.v, self.r, self.q, self.t)
                    F = sb_F(eta, self.x, self.s, self.h, self.v, self.r, self.q, self.t, self.is_kop_delay)
                    result = self.p * (A - B + C - D) + F
                if self.k < self.h:
                    F = sb_F(eta, self.x, self.s, self.h, self.v, self.r, self.q, self.t, self.is_kop_delay)
                    result = F # self.p * 0.0 + F
        else:
            self.error_message = "障碍类型 %d 不存在！" % self.barrier_type
            raise Exception(self.error_message)
        return result

    def CalcPayoff(self):
        result = 0.0
        if self.barrier_type == self.up_in:
            if self.is_call == True: # 看涨认购
                if self.s >= self.h: # s >= h 已 向上敲入
                    result = max(self.s - self.k, 0.0)
                else: # s < h 未 向上敲入
                    result = self.x
            else: # 看跌认沽
                if self.s >= self.h: # s >= h 已 向上敲入
                    result = max(self.k - self.s, 0.0)
                else: # s < h 未 向上敲入
                    result = self.x
        elif self.barrier_type == self.down_in:
            if self.is_call == True: # 看涨认购
                if self.s <= self.h: # s <= h 已 向下敲入
                    result = max(self.s - self.k, 0.0)
                else: # s > h 未 向下敲入
                    result = self.x
            else: # 看跌认沽
                if self.s <= self.h: # s <= h 已 向下敲入
                    result = max(self.k - self.s, 0.0)
                else: # s > h 未 向下敲入
                    result = self.x
        elif self.barrier_type == self.up_out:
            if self.is_call == True: # 看涨认购
                if self.s >= self.h: # s >= h 已 向上敲出
                    result = self.x
                else: # s < h 未 向上敲出
                    result = max(self.s - self.k, 0.0)
            else: # 看跌认沽
                if self.s >= self.h: # s >= h 已 向上敲出
                    result = self.x
                else: # s < h 未 向上敲出
                    result = max(self.k - self.s, 0.0)
        elif self.barrier_type == self.down_out:
            if self.is_call == True: # 看涨认购
                if self.s <= self.h: # s <= h 已 向下敲出
                    result = self.x
                else: # s > h 未 向下敲出
                    result = max(self.s - self.k, 0.0)
            else: # 看跌认沽
                if self.s <= self.h: # s <= h 已 向下敲出
                    result = self.x
                else: # s > h 未 向下敲出
                    result = max(self.k - self.s, 0.0)
        else:
            self.error_message = "障碍类型 %d 不存在！" % self.barrier_type
            raise Exception(self.error_message)
        return result
