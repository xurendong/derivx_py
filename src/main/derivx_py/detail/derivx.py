
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

import barrier_single
import barrier_double
import digital_simple
import vanilla_european
import vanilla_american
import autocall_phoenix
import autocall_snowball

g_version = "V0.1.0-Beta Build 20211103"

def Version():
    return g_version

def Barrier(type):
    type = type.lower()
    if type == "single":
        return barrier_single.Barrier_Single()
    elif type == "double":
        return barrier_double.Barrier_Double()

def Digital(type):
    type = type.lower()
    if type == "gap":
        return digital_simple.Digital_Gap()
    elif type == "cashornothing":
        return digital_simple.Digital_CashOrNothing()
    elif type == "assetornothing":
        return digital_simple.Digital_AssetOrNothing()
    elif type == "supershare":
        return digital_simple.Digital_SuperShare()

def Vanilla(type):
    type = type.lower()
    if type == "european":
        return vanilla_european.Vanilla_European()
    elif type == "american":
        return vanilla_american.Vanilla_American()

def Autocall(type):
    type = type.lower()
    if type == "phoenix":
        return autocall_phoenix.Autocall_Phoenix()
    elif type == "snowball":
        return autocall_snowball.Autocall_Snowball()
