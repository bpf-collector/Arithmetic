# -*- coding: utf-8 -*-
'''
 * @Author       : bpf
 * @Date         : 2020-09-19 17:04:32
 * @version      : 1.0
 * @Description  : 测试GeneralFormular类的性能 运行1e6次
 * @LastEditTime : 2020-09-21 15:07:34
'''
import datetime
from formula import OPT, GeneralFormular, ComputeFormular

def getRandomIntOperandTest(gf):
    '''
     * 测试操作数
    '''
    print(gf.getRandomIntOperand())


def getRandomOperatorTest(gf):
    '''
     * 测试运算符
    '''
    print(gf.getRandomOperator())


def catFormulaTest_2(gf):
    '''
     * 连接2个操作数
    '''
    s1 = gf.catFormula(gf.getRandomIntOperand(), gf.getRandomOperator(), gf.getRandomIntOperand())
    # print(s1)
# 1e6
# oper_num = 2  0:00:22.106145; 0:00:24.205105; 0:00:23.322774; 0:00:21.820833; 0:00:21.720548; 0:00:21.972804;


def catFormulaTest_3(gf):
    '''
     * 连接3个操作数
    '''
    s1 = catFormulaTest_2(opt)
    s2 = gf.catFormula(s1, gf.getRandomOperator(), gf.getRandomIntOperand())
    # print(s2)
# 1e6
# oper_num = 3  0:00:39.107180; 0:00:37.459140; 0:00:39.419202; 0:00:38.641602; 0:00:41.358436; 0:00:38.216952;


def getOriginFormularTest(gf):
    '''
     * 生成源算式
    '''
    s = gf.getOriginFormular()
    # print(s)
# 1e6
# oper_num = 2  0:00:25.417081; 0:00:25.144765; 0:00:25.671593;
# oper_num = 3  0:00:38.823994; 0:00:44.753355; 0:00:39.408033; 0:00:40.876879; 0:00:40.043860; 0:00:40.421104
# oper_num = 5  0:01:33.783633; 0:01:23.847334; 0:01:23.585094;
# oper_num = 10 0:02:25.813135; 0:02:22.253166; 0:02:26.389291;

def insertBracketTest(gf):
    '''
     * 加括号
    '''
    s = gf.insertBracket(gf.getOriginFormular())
    # print(s)
# 1e6
# oper_num = 5  0:02:04.309764; 0:02:14.685606; 0:02:15.070132;
# oper_num = 10 0:03:50.393577; 0:03:44.217675;

def replaceFractionTest(gf):
    '''
     * 替换分数
    '''
    s = gf.replaceFraction(gf.insertBracket(gf.getOriginFormular()))
    # print(s)
# 1e6
# oper_num = 5  0:02:13.869587; 

def gf_solveTest(gf):
    s = gf.solve()
# 1e6
# version 1.0 oper_num = 5  0:00:48.304376; 0:00:49.523814; 0:00:45.649577;
# version 2.0 oper_num = 5  0:00:40.939863; 0:00:37.203209; 0:00:38.834361;

def cf_solveTest(cf, formular):
    s = cf.solve(formular)
# 1e6
# version 1.0 oper_num = 5  0:01:23.161481; 0:01:26.414998; 0:01:25.195089;
# version 2.0 oper_num = 5  0:01:20.533413; 0:01:20.834751; 0:01:21.405273;

if __name__ == "__main__":
    opt = OPT(oper_num=5, has_fraction=True)
    gf = GeneralFormular(opt)
    cf = ComputeFormular()

    formulars = []
    
    start = datetime.datetime.now()
    for i in range(int(1e6)):
        # getRandomIntOperandTest(gf)
        # getRandomOperatorTest(gf)
        # catFormulaTest_2(gf)
        # catFormulaTest_3(gf)
        # getOriginFormularTest(gf)
        # insertBracketTest(gf)
        # replaceFractionTest(gf)
        # gf_solveTest(gf)
        # formulars.append(gf.solve())
        cf_solveTest(cf, gf.solve())
        pass

    print("Time: {}".format(datetime.datetime.now() - start))

    start = datetime.datetime.now()
    for i in formulars:
        cf_solveTest(cf, i)

    print("Time: {}".format(datetime.datetime.now() - start))