# -*- coding: utf-8 -*-
'''
 * @Author       : bpf
 * @Date         : 2020-09-19 15:57:48
 * @version      : 1.0
 * @Description  : 实现四则运算
 * @LastEditTime : 2020-09-24 00:31:56
'''

import random
import datetime
import argparse
import re
from fractions import Fraction

def OPT(up_limit=10, oper_num=2, oper_variety=4, has_fraction=True):
    '''
     * 设置参数

     * @param up_limit {int} 操作数数值上限

     * @param oper_num {int} 操作数个数

     * @param oper_variety {int} 运算符种类

     * @param has_fraction {bool} 是否带有分数
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

    return parse.parse_args(args=[])

class GeneralFormular:
    '''
     * 生成算式
     
     * @param opt {OPT} 参数
    '''
    def __init__(self, opt):
        self.opt = opt

    # @profile
    def catFormula(self, operand1, operator, operand2):
        '''
        * 连接算式

        * @param operand1 {str} 操作数1
        
        * @param opertor {str} 运算符

        * @param operand2 {str} 操作数2

        * @return {str}
        '''

        return "{}{}{}".format(operand1, operator, operand2)

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

        # 保证分数为真分数
        if num01 < num02:
            return str(num01) + "/" + str(num02)
        else:
            return str(num02) + "/" + str(num01)

    # @profile
    def getRandomOperator(self):
        '''
        * 返回随机运算符

        * @return {str}
        '''
        index = random.randint(0, self.opt.oper_variety-1)
        if index == 0:
            return '+'
        elif index == 1:
            return '-'
        elif index == 2:
            return '×'
        else:
            return '÷'

    # @profile
    def getOriginFormular(self):
        '''
        * 生成整数源算式

        * @return {str} 
        '''
        # 通过self.opt.oper_num控制操作数个数，循环调用catFormula()方法构造算式
        tmp = self.getRandomIntOperand()
        for i in range(self.opt.oper_num-1):
            tmp = self.catFormula(tmp, self.getRandomOperator(), self.getRandomIntOperand())

        # 去掉'÷0'
        while(True):
            if '÷0' in tmp:
                tmp = tmp.replace('÷0', '÷'+str(self.getRandomIntOperand()))
            else:
                break

        return tmp

    # @profile
    def insertBracket(self, formular):
        '''
         * 插入括号

         * @param formular {str} 源算式

         * @return {str} 
        '''
        # print(formular)

        # 若只包含+号 或 只有两个操作数 则不用加括号
        if self.opt.oper_variety <= 2 or self.opt.oper_num == 2:
            return formular
        # 若不包含×÷ 则不用加括号
        if '×' not in formular and '÷' not in formular:
            return formular
        
        # 操作数列表
        operand_list = re.split("[-|+|×|÷]", formular)
        # 操作符列表
        operator_list = re.split("[!0-9]", formular)
        # 去掉空字符
        while '' in operator_list:
            operator_list.remove('')
        # print(operand_list, operator_list)

        # 存储添加括号的算式
        new_formular = ""
        
        # flag表示是否已存在左括号，作用在于构造出一对括号
        flag = 0

        # 添加括号
        for i in range(len(operator_list)):
            oper = operator_list.pop(0)
            # 若下一个符号为 + or - , 则插入括号
            if oper == '-' or oper == '+':
                if flag == 0:
                    new_formular += "("
                    flag = 1
                new_formular += (str(operand_list.pop(0)) + str(oper))
            else:
                new_formular += str(operand_list.pop(0))

                if flag == 1:
                    new_formular += ")"
                    flag = 0
                
                new_formular += str(oper)
            # print(operand_list, operator_list, new_formular)
        
        new_formular += str(operand_list.pop(0))
        if flag == 1:
            new_formular += ")"
        
        return new_formular
    
    # @profile
    def replaceFraction(self, formular):
        '''
         * 带入分数

         * @param formular {str} 源算式，可能包含括号

         * @return {str} 
        '''

        # 带入分数个数
        fraction_num = 1
        if self.opt.oper_num > 2:
            fraction_num = (self.opt.oper_num - 1) / 2
        # 操作数列表
        operand_list = re.split("[-|+|×|÷|(|)]", formular)
        # 去掉空字符
        while '' in operand_list:
            operand_list.remove('')
        index = random.randint(0, len(operand_list)-1)

        formular = formular.replace(str(operand_list[index]), self.getRandomFractionOperand())

        return formular

    # @profile
    def solve(self):
        '''
         * 整合生成算式的后缀表达式，带括号

         * @return {str} 
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
    def getPostFormular(self, formular):
        '''
        * 中缀表达式转为后缀表达式

        * @param formular {str} 中缀表达式
        
        * @return {str} 
        '''
        # 运算符栈
        operator_stack = []
        
        # 后缀表达式
        post_formular = ""

        # 中缀表达式转为后缀表达式
        i = 0
        while i < len(formular):
            char = formular[i]
            # print("1: ", i, char, operator_stack, post_formular)
            if char == '(':
                operator_stack.append(char)
                i += 1
                # print("2: ", i, operator_stack, post_formular)
            elif char == ')':
                tmp_char = operator_stack.pop()
                while tmp_char != '(':
                    post_formular += tmp_char
                    if len(operator_stack) != 0:
                        tmp_char = operator_stack.pop()
                    else:
                        break
                i += 1
                # print("3: ", i, operator_stack, post_formular)
            elif char == '+' or char == '-':
                try:
                    tmp_char = operator_stack.pop()
                except Exception as e:
                    pass
                while len(operator_stack) != 0:
                    if tmp_char != '(':
                        post_formular += tmp_char
                        if len(operator_stack) != 0:
                            tmp_char = operator_stack.pop()
                        else:
                            break
                    else:
                        operator_stack.append(tmp_char)
                        break
                operator_stack.append(char)
                i += 1
                # print("4: ", i, operator_stack, post_formular)
            elif char == '×' or char == '÷':
                while len(operator_stack) != 0:
                    tmp_char = operator_stack.pop()
                    if tmp_char== '×' or tmp_char == '÷':
                        post_formular += tmp_char
                        if len(operator_stack) != 0:
                            tmp_char = operator_stack.pop()
                        else:
                            break
                    else:
                        break
                operator_stack.append(char)
                i += 1
                # print("5: ", i, operator_stack, post_formular)
            # 存在数字时
            else:
                # print("6: ", i, operator_stack, post_formular)
                while char >= '0' and char <= '9' or char == '/':
                    post_formular += char
                    i += 1
                    if i < len(formular):
                        char = formular[i]
                    else:
                        break
                post_formular += '#'
                # print("7: ", i, operator_stack, post_formular)

        # 若符号栈不为空则循环
        while len(operator_stack) != 0:
            tmp_char = operator_stack.pop(0)
            post_formular += tmp_char
            # print("8: ", i, operator_stack, tmp_char)
        
        # print(post_formular)
        return post_formular
    
    # @profile
    def calcFormular(self, formular):
        '''
         * 计算算式的值

         * @param formular {str} 后缀表达式

         * @return {str} 
        '''
        # 操作数栈
        operand_stack = []
        i = 0
        while i < len(formular):
            if formular[i] == '+':
                num01 = operand_stack.pop()
                num02 = operand_stack.pop()
                result = Fraction(num02) + Fraction(num01)
                operand_stack.append(result.__str__())
            elif formular[i] == '-':
                num01 = operand_stack.pop()
                num02 = operand_stack.pop()
                result = Fraction(num02) - Fraction(num01)
                operand_stack.append(result.__str__())
            elif formular[i] =='×':
                num01 = operand_stack.pop()
                num02 = operand_stack.pop()
                result = Fraction(num02) * Fraction(num01)
                operand_stack.append(result.__str__())
            elif formular[i] == '÷':
                num01 = operand_stack.pop()
                num02 = operand_stack.pop()
                try:
                    result = Fraction(num02) / Fraction(num01)
                    operand_stack.append(result.__str__())
                except Exception as e:
                    # print('Error: 除零错误！')
                    return "NaN"
            else:
                number = ""
                while formular[i] >= '0' and formular[i] <= '9' or formular[i] == '/':
                    number += formular[i]
                    if i < len(formular):
                        i += 1
                    else:
                        i -= 1
                        break
                operand_stack.append(number)
            
            i += 1

        return operand_stack.pop()
    
    # @profile
    def solve(self, formular):
        '''
         * 整合计算中缀表达式的值

         * @param formular {str} 后缀表达式

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
    print("中缀式：", fra_formular)
    value = cf.solve(fra_formular)
    print("结果：", value)