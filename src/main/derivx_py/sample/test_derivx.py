
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

import derivx

def Test_DerivX():
    print(derivx.Version())

def Test_Barrier():
    barrier = derivx.Barrier("Single")
    
    barrier = derivx.Barrier("Double")

def Test_Digital():
    digital = derivx.Digital("CashOrNothing")
    
    digital = derivx.Digital("AssetOrNothing")
    
    digital = derivx.Digital("SuperShare")

def Test_Vanilla():
    vanilla = derivx.Vanilla("American")
    
    vanilla = derivx.Vanilla("European")

def Test_Autocall():
    autocall = derivx.Autocall("Booster")
    
    autocall = derivx.Autocall("Phoenix")
    
    autocall = derivx.Autocall("Snowball")

if __name__ == "__main__":
    Test_DerivX()
    Test_Barrier()
    Test_Digital()
    Test_Vanilla()
    Test_Autocall()
