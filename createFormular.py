# -*- coding: utf-8 -*-
'''
 * @Author       : bpf
 * @Date         : 2020-09-20 18:51:37
 * @Description  : 生成算式
 * @LastEditTime : 2020-09-21 09:35:06
'''

import datetime
import os
from formula import OPT, GeneralFormular, ComputeFormular

def getInput():
    '''
     * 获取输入参数
    '''
    print("{:^18} | {:^5} | {:^8}".format("参数", "数值范围", "请输入"))
    print("{0:-<21}+{0:-<11}+{0:-<12}".format('-'))
    n = input("{:>14} | {:9} | ".format("生成算式数量", "[>=1]"))
    while True:
        try:
            n = abs(int(n))
            break
        except Exception as e:
            print("[Eror]: Input illegal! Please input again...  ", end="")
            n = input()
    
    up_limit = input("{:>16} | {:9} | ".format("数值上限", "[>=10]"))
    while True:
        try:
            up_limit = abs(int(up_limit))
            break
        except Exception as e:
            print("[Eror]: Input illegal! Please input again...  ", end="")
            up_limit = input()
    
    oper_num = input("{:>15} | {:9} | ".format("操作数个数", "[>=2]"))
    while True:
        try:
            oper_num = abs(int(oper_num))
            if oper_num < 2:
                oper_num = 2
                print("[Eror]: Input illegal! Use default value 2.")
            break
        except Exception as e:
            print("[Eror]: Input illegal! Please input again...  ", end="")
            oper_num = input()
    
    oper_variety = input("{:>15} | {:9} | ".format("运算符种数", "[1~4]"))
    while True:
        try:
            oper_variety = abs(int(oper_variety))
            if oper_variety < 1 or oper_variety > 4:
                oper_variety = 4
                print("[Eror]: Input illegal! Use default value 4.")
            break
        except Exception as e:
            print("[Eror]: Input illegal! Please input again...  ", end="")
            oper_variety = input()
    
    has_fraction = input("{:>14} | {:9} | ".format("是否包含分数", "[0, 1]"))
    while True:
        try:
            has_fraction = abs(int(has_fraction))
            if has_fraction != 0 and has_fraction != 1:
                has_fraction = 0
                print("[Eror]: Input illegal! Use default value 0.")
            break
        except Exception as e:
            print("[Eror]: Input illegal! Please input again...  ", end="")
            has_fraction = input()
    
    print("{0:-<46}".format('-'))

    return int(n), int(up_limit), int(oper_num), int(oper_variety), int(has_fraction)

def getOutputMode():
    '''
     * 获取输出模式
    '''
    print("  算式生成中 ...")
    print("{0:-<46}".format('-'))
    print("{:^37}".format("请选择算式输出模式"))
    print("    1. 普通模式")
    print("    2. 问答模式")
    print("    3. 文件模式")
    mode = input("    请选择：")
    print("{0:-<46}".format('-'))
    try:
        mode = abs(int(mode))
    except Exception as e:
        mode = 1
    
    return mode

def displayFormular(mode, formulars, results):
    '''
     * 输出算式
    '''
    count = 0
    if mode == 1:
        for i in range(len(formulars)):
            print(formulars[i], results[i])
    elif mode == 2:
        start = datetime.datetime.now()
        for i in range(len(formulars)):
            # print(,end="")
            result = input("第{}题：".format(i+1) + formulars[i])
            if result == results[i]:
                count += 1
                flag = "正确✔✔✔"
            else:
                flag = "错误×"
            print("    正确答案：{}  回答{}".format(results[i], flag))
        
        print("\n正确率为：{}/{}({:.2f}%)".format(count, len(formulars), 100*float(count/len(formulars))))
        print("耗时：{}".format(datetime.datetime.now() - start))
    else:
        filepath = input("  请输入文件路径：")
        if not filepath.endswith(".txt"):
            portion = os.path.splitext(filepath)
            filepath = portion[0] + ".txt"
            print("[Eror]: Input illegal! Use default value <{}>.".format(filepath))
        try:
            with open(filepath, 'w+') as f:
                for i in range(len(formulars)):
                    f.write(formulars[i] + results[i] + "\n")
            print("  文件写入成功")
            print("{0:-<46}".format('-'))
        except Exception as e:
            print("Error: ", e)
            print("{0:-<46}".format('-'))

        



if __name__ == "__main__":
    n, up_limit, oper_num, oper_variety, has_fraction = getInput()
    # n, up_limit, oper_num, oper_variety, has_fraction = 5, 20, 4, 4, 0
    opt = OPT(up_limit, oper_num, oper_variety, has_fraction)

    gf = GeneralFormular(opt)
    cf = ComputeFormular()

    formulars = []
    results = []
    for i in range(int(n)):
        f = gf.solve()
        formulars.append(" ".join(i for i in f) + " = ")
        results.append(cf.solve(f))

    mode = getOutputMode()
    displayFormular(mode, formulars, results)
