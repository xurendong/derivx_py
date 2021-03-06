
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
    n = sb_n(r, v, u) # ????????????
    if is_kop_delay == True: # ????????????
        n = (r ** 2 + v ** 4 / 4.0 + r * v ** 2) ** 0.5 / v ** 2
    z = sb_z(s, h, v, n, t)
    return x * ((h / s) ** (u + n) * stats.norm.cdf(eta * z) + (h / s) ** (u - n) * stats.norm.cdf(eta * (z - 2.0 * n * v * t ** 0.5)))

class Config(object):
    def __init__(self, s, h, k, x, v, r, q, t, p, is_call, is_knock, is_kop_delay, barrier_type):
        self.s = s # ????????????
        self.h = h # ????????????
        self.k = k # ????????????
        self.x = x # ?????????????????????????????????
        self.v = v # ?????????
        self.r = r # ???????????????
        self.q = q # ???????????????
        self.t = t # ??????????????????
        self.p = p # ????????????????????????????????????????????????????????????
        self.is_call = is_call # ????????????
        self.is_kop_delay = is_kop_delay # ??????????????????????????????????????????
        self.barrier_type = barrier_type # ????????????

    def ToArgs(self):
        return self.__dict__

class Barrier_Single(object):
    def __init__(self):
        self.s = 0.0 # ????????????
        self.h = 0.0 # ????????????
        self.k = 0.0 # ????????????
        self.x = 0.0 # ?????????????????????????????????
        self.v = 0.0 # ?????????
        self.r = 0.0 # ???????????????
        self.q = 0.0 # ???????????????
        self.t = 0.0 # ??????????????????
        self.p = 0.0 # ????????????????????????????????????????????????????????????
        self.is_call = True # ????????????
        self.is_kop_delay = False # ??????????????????????????????????????????
        self.barrier_type = 0 # ????????????
        
        self.up_in    = 1 # ????????????
        self.down_in  = 2 # ????????????
        self.up_out   = 3 # ????????????
        self.down_out = 4 # ????????????
        
        self.error_message = ""

    def GetError(self):
        return self.error_message

    def InitArgs(self, config): # config???dict
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
            self.error_message = "???????????????????????????%s" % e
        return -1

    def CalcPrice(self):
        result = 0.0
        if self.barrier_type == self.up_in:
            if self.is_call == True: # ????????????
                eta = -1.0
                phi = 1.0
                # k == h ??????????????? result ??????
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
            else: # ????????????
                eta = -1.0
                phi = -1.0
                # k == h ??????????????? result ??????
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
            if self.is_call == True: # ????????????
                eta = 1.0
                phi = 1.0
                # k == h ??????????????? result ??????
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
            else: # ????????????
                eta = 1.0
                phi = -1.0
                # k == h ??????????????? result ??????
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
            if self.is_call == True: # ????????????
                eta = -1.0
                phi = 1.0
                # k == h ??????????????? result ??????
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
            else: # ????????????
                eta = -1.0
                phi = -1.0
                # k == h ??????????????? result ??????
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
            if self.is_call == True: # ????????????
                eta = 1.0
                phi = 1.0
                # k == h ??????????????? result ??????
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
            else: # ????????????
                eta = 1.0
                phi = -1.0
                # k == h ??????????????? result ??????
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
            self.error_message = "???????????? %d ????????????" % self.barrier_type
            raise Exception(self.error_message)
        return result

    def CalcPayoff(self):
        result = 0.0
        if self.barrier_type == self.up_in:
            if self.is_call == True: # ????????????
                if self.s >= self.h: # s >= h ??? ????????????
                    result = max(self.s - self.k, 0.0)
                else: # s < h ??? ????????????
                    result = self.x
            else: # ????????????
                if self.s >= self.h: # s >= h ??? ????????????
                    result = max(self.k - self.s, 0.0)
                else: # s < h ??? ????????????
                    result = self.x
        elif self.barrier_type == self.down_in:
            if self.is_call == True: # ????????????
                if self.s <= self.h: # s <= h ??? ????????????
                    result = max(self.s - self.k, 0.0)
                else: # s > h ??? ????????????
                    result = self.x
            else: # ????????????
                if self.s <= self.h: # s <= h ??? ????????????
                    result = max(self.k - self.s, 0.0)
                else: # s > h ??? ????????????
                    result = self.x
        elif self.barrier_type == self.up_out:
            if self.is_call == True: # ????????????
                if self.s >= self.h: # s >= h ??? ????????????
                    result = self.x
                else: # s < h ??? ????????????
                    result = max(self.s - self.k, 0.0)
            else: # ????????????
                if self.s >= self.h: # s >= h ??? ????????????
                    result = self.x
                else: # s < h ??? ????????????
                    result = max(self.k - self.s, 0.0)
        elif self.barrier_type == self.down_out:
            if self.is_call == True: # ????????????
                if self.s <= self.h: # s <= h ??? ????????????
                    result = self.x
                else: # s > h ??? ????????????
                    result = max(self.s - self.k, 0.0)
            else: # ????????????
                if self.s <= self.h: # s <= h ??? ????????????
                    result = self.x
                else: # s > h ??? ????????????
                    result = max(self.k - self.s, 0.0)
        else:
            self.error_message = "???????????? %d ????????????" % self.barrier_type
            raise Exception(self.error_message)
        return result
