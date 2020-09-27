# -*- coding: utf-8 -*-
'''
 * @Author       : bpf
 * @Date         : 2020-09-19 15:57:48
 * @version      : 2.0
 * @Description  : 实现四则运算
 * @LastEditTime : 2020-09-24 00:31:56
'''

import random
import datetime
import argparse
import re
from fractions import Fraction

def OPT(up_limit=10, oper_num=2, oper_variety=4, has_fraction=True, be_negetive=False):
    '''
     * 设置参数

     * @param up_limit {int} 操作数数值上限

     * @param oper_num {int} 操作数个数

     * @param oper_variety {int} 运算符种类

     * @param has_fraction {bool} 是否带有分数

     * @param be_negative {bool} 可否存在负数
    '''
    parse = argparse.ArgumentParser()
    # 操作数数值上限
    parse.add_argument('--up_limit', type=int, default=up_limit)
    # 操作数个数
    parse.add_argument('--oper_num', type=int, default=oper_num)
    # 运算符种类
    parse.add_argument('--oper_variety', type=int, default=oper_variety)
    # 是否带有分数
    parse.add_argument('--has_fraction', type=bool, default=has_fraction)
    # 可否存在负数
    parse.add_argument('--be_negative', type=bool, default=be_negetive)

    return parse.parse_args(args=[])

class GeneralFormular:
    '''
     * 生成算式
     
     * @param opt {OPT} 参数
    '''
    def __init__(self, opt):
        self.opt = opt
        # 定义运算符
        self.operator = ['+', '-', '×', '÷']

    # @profile
    def catFormula(self, operand1, operator, operand2):
        '''
        * 连接算式

        * @param operand1 {str} 操作数1
        
        * @param opertor {str} 运算符

        * @param operand2 {str} 操作数2

        * @return {str}
        '''

        return "{}#{}#{}".format(operand1, operator, operand2)

    # @profile
    def getRandomIntOperand(self):
        '''
        * 返回随机整数操作数
        
        * @return {int} 
        '''
        return random.randint(0, self.opt.up_limit)
    
    # @profile
    def getRandomFractionOperand(self):
        '''
        * 返回随机分数操作数
        
        * @return {str} 
        '''
        # 生成两个整数，一个作为分子，一个作为分母
        num01 = self.getRandomIntOperand()
        num02 = self.getRandomIntOperand()
        while num01 == num02 or num02==0:
            num02 = self.getRandomIntOperand()
        while num01 == 0:
            num01 = self.getRandomIntOperand()

        # 保证分数为真分数, 化简
        if num01 < num02:
            return Fraction(num01, num02).__str__()
        else:
            return Fraction(num02, num01).__str__()

    # @profile
    def getRandomOperator(self):
        '''
        * 返回随机运算符

        * @return {str}
        '''
        index = random.randint(0, self.opt.oper_variety-1)
        return self.operator[index]

    # @profile
    def getOriginFormular(self):
        '''
        * 生成整数源算式

        * @return {list} 
        '''
        # 通过self.opt.oper_num控制操作数个数，循环调用catFormula()方法构造算式
        formular = self.getRandomIntOperand()
        for i in range(self.opt.oper_num-1):
            formular = self.catFormula(formular, self.getRandomOperator(), self.getRandomIntOperand())

        # 去掉'÷0'
        while(True):
            if '÷#0' in formular:
                formular = formular.replace('÷#0', '÷#' + str(self.getRandomIntOperand()))
            else:
                break
        # 通过'#'分割生成列表
        formular_list = formular.split('#')

        return formular_list

    # @profile
    def insertBracket(self, formular_list):
        '''
         * 插入括号

         * @param formular_list {list} 源算式列表

         * @return {list} 
        '''
        # print(formular)

        # 若只包含+号 或 只有两个操作数 则不用加括号
        if self.opt.oper_variety <= 2 or self.opt.oper_num == 2:
            return formular_list
        # 若不包含×÷ 则不用加括号
        if '×' not in formular_list and '÷' not in formular_list:
            return formular_list

        # 存储添加括号的算式
        new_formular_list = []
        
        # flag表示是否已存在左括号，作用在于构造出一对括号
        flag = 0

        # 添加括号
        while(len(formular_list) > 1):
            oper = formular_list.pop(1)
            # 若下一个符号为 + or - , 则插入括号
            if oper == '-' or oper == '+':
                if flag == 0:
                    new_formular_list.append("(")
                    flag = 1
                new_formular_list.append(formular_list.pop(0))
                new_formular_list.append(oper)
            else:
                new_formular_list.append(formular_list.pop(0))

                if flag == 1:
                    new_formular_list.append(")")
                    flag = 0
                
                new_formular_list.append(oper)
            # print(operand_list, operator_list, new_formular)
        
        new_formular_list.append(formular_list.pop(0))
        if flag == 1:
            new_formular_list.append(")")
        
        return new_formular_list
    
    # @profile
    def replaceFraction(self, formular_list):
        '''
         * 带入分数

         * @param formular_list {list} 源算式列表，可能包含括号

         * @return {list} 
        '''

        # 带入分数个数
        fraction_num = 1
        if self.opt.oper_num > 2:
            fraction_num = (self.opt.oper_num - 1) / 2
        index = random.randint(0, len(formular_list)-1)

        interval = 1
        while True:
            if formular_list[index].isdigit():
                break
            elif formular_list[index - interval].isdigit():
                index -= interval
                break
            elif formular_list[index + interval].isdigit():
                index += interval
                break
            else:
                interval += 1
        formular_list[index] = self.getRandomFractionOperand()

        return formular_list

    # @profile
    def solve(self):
        '''
         * 整合生成算式的后缀表达式，带括号

         * @return {list} 
        '''
        # 生成原生算式
        ori_formular = self.getOriginFormular()
        # 添加括号
        bra_formular = self.insertBracket(ori_formular)
        # 带入分数
        if self.opt.has_fraction:
            bra_formular = self.replaceFraction(bra_formular)

        return bra_formular

class ComputeFormular:
    '''
     * 计算算式的值
    '''
    def __init__(self):
        pass
    
    # @profile
    def getPostFormular(self, formular_list):
        '''
        * 中缀表达式转为后缀表达式

        * @param formular_list {list} 中缀表达式
        
        * @return {list} 
        '''
        # 运算符优先级
        priority = {'×': 3, '÷': 3, '+': 2, '-': 2, '(': 1}

        # 运算符栈
        operator_stack = []
        
        # 后缀表达式
        post_formular_list = []

        # 中缀表达式转为后缀表达式
        while formular_list:
            char = formular_list.pop(0)
            if char == '(':
                operator_stack.append(char)
            elif char == ')':
                oper_char = operator_stack.pop()
                while oper_char != '(':
                    post_formular_list.append(oper_char)
                    oper_char = operator_stack.pop()
            elif char in '+-×÷':
                while operator_stack and priority[operator_stack[-1]] >= priority[char]:
                    post_formular_list.append(operator_stack.pop())
                operator_stack.append(char)
            else:
                post_formular_list.append(char)

        # 若符号栈不为空则循环
        while operator_stack:
            post_formular_list.append(operator_stack.pop())
        
        # print(post_formular)
        return post_formular_list
        
    # @profile
    def compute(self, char, num01, num02):
        '''
        * 计算算式的值

        * @param char {str} 运算符
        
        * @param num01 {str} 第二个数字，可能为分数

        * @param num02 {str} 第二个数字，可能为分数
        
        * @return {str}
        '''
        if char == '+':
            return (Fraction(num02) + Fraction(num01)).__str__()
        elif char == '-':
            return (Fraction(num02) - Fraction(num01)).__str__()
        elif char == '×':
            return (Fraction(num02) * Fraction(num01)).__str__()
        elif char == '÷':
            try:
                return (Fraction(num02) / Fraction(num01)).__str__()
            except Exception as e:
                # print("Error: ", e)
                return "NaN"

    # @profile
    def calcFormular(self, post_formular_list):
        '''
         * 计算算式的值

         * @param post_formular_list {list} 后缀表达式

         * @return {str} 
        '''
        # 操作数栈
        operand_stack = []

        while post_formular_list:
            char = post_formular_list.pop(0)
            if char in '+-×÷':
                result = self.compute(char, operand_stack.pop(), operand_stack.pop())
                if result == "NaN":
                    return result
                operand_stack.append(result)
            else:
                operand_stack.append(char)

        return operand_stack.pop()
    
    # @profile
    def solve(self, formular):
        '''
         * 整合计算中缀表达式的值

         * @param formular {list} 后缀表达式

         * @return {str} 
        '''
        # 转为后缀表达式
        post_formular = self.getPostFormular(formular)
        # 计算值
        value = self.calcFormular(post_formular)

        return value


if __name__ == "__main__":
    opt = OPT(up_limit=10, oper_num=5, oper_variety=4, has_fraction=True)
    gf = GeneralFormular(opt)
    # gf.getRandomIntOperand()
    # gf.getRandomFractionOperand()
    # gf.getRandomOperator()
    # formular = gf.getOriginFormular()
    # new_formular = gf.insertBracket(formular)
    # fra_formular = gf.replaceFraction(new_formular)
    # print("源算式：", formular)
    # print("加括号：", new_formular)
    # print("换分数：", fra_formular)

    cf = ComputeFormular()
    # post_formular = cf.getPostFormular(fra_formular)
    # value = cf.calcFormular(post_formular)
    # print("后缀式：", post_formular)
    # print("结果：", value)

    fra_formular = gf.solve()
    print(" ".join(i for i in fra_formular), end=" = ")
    value = cf.solve(fra_formular)
    print(value)