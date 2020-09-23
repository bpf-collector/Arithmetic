# -*- coding: utf-8 -*-
'''
 * @Author       : bpf
 * @Date         : 2020-09-20 18:51:37
 * @Description  : 生成算式
 * @LastEditTime : 2020-09-21 09:35:06
'''

from formula import OPT, GeneralFormular, ComputeFormular

if __name__ == "__main__":
    print("{:^18} | {:^5} | {:^8}".format("参数", "数值范围", "请输入"))
    print("{0:-<21}+{0:-<11}+{0:-<12}".format('-'))
    n = input("{:>14} | {:9} | ".format("生成算式数量", "[>=1]"))
    up_limit = input("{:>16} | {:9} | ".format("数值上限", "[>=10]"))
    oper_num = input("{:>15} | {:9} | ".format("操作数个数", "[>=2]"))
    oper_variety = input("{:>15} | {:9} | ".format("运算符种数", "[1~4]"))
    has_fraction = int(input("{:>14} | {:9} | ".format("是否包含分数", "[0, 1]")))
    print("{0:-<46}".format('-'))
    opt = OPT(up_limit, oper_num, oper_variety, has_fraction)

    gf = GeneralFormular(opt)
    cf = ComputeFormular()

    formulars = {}
    for i in range(int(n)):
        f = gf.solve()
        s = cf.solve(f)
        formulars[i+1] = f + " = " + s
        print(formulars[i+1])
