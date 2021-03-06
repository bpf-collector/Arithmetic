# -*- coding: utf-8 -*-
'''
 * @Author       : bpf
 * @Date         : 2020-09-20 17:13:55
 * @version      : 1.0
 * @Description  : 单元测试
 * @LastEditTime : 2020-09-21 10:52:12
'''

import unittest
from formula import OPT, GeneralFormular, ComputeFormular

class FormulaUnitTest(unittest.TestCase):
    def test_gf_catFormular(self):
        '''
         * 测试拼接算式 
        '''
        gf = GeneralFormular(OPT())
        self.assertEqual(gf.catFormula("12", "+", "34"), "12#+#34")
        self.assertEqual(gf.catFormula("23", "+", "456"), "23#+#456")
        self.assertEqual(gf.catFormula("12", "+", "32"), "12#+#32")

    def test_cf_getPostFormular(self):
        '''
         * 测试中缀表达式转为后缀表达
        '''
        cf = ComputeFormular()
        self.assertEqual(cf.getPostFormular(['3', '+', '7']), ['3', '7', '+'])
        self.assertEqual(cf.getPostFormular(['3', '×', '(', '7', '+', '2', '+', '1', ')']), ['3', '7', '2', '+', '1', '+', '×'])
        self.assertEqual(cf.getPostFormular(['6', '×', '(', '2', '+', '1', ')', '÷', '(', '9', '-', '2', '+', '3', ')']), ['6', '2', '1', '+', '×', '9', '2', '-', '3', '+', '÷'])
        self.assertEqual(cf.getPostFormular(['6', '×', '(', '2', '+', '1', ')', '÷', '0']), ['6', '2', '1', '+', '×', '0', '÷'])
    
    def test_cf_calcFormular(self):
        '''
         * 测试后缀表达式计算为数值
        '''
        cf = ComputeFormular()
        self.assertEqual(cf.calcFormular(['3', '7', '+']), "10")
        self.assertEqual(cf.calcFormular(['3', '7', '2', '+', '1', '+', '×']), "30")
        self.assertEqual(cf.calcFormular(['6', '2', '1', '+', '×', '9', '2', '-', '3', '+', '÷']), "9/5")
        self.assertEqual(cf.calcFormular(['6', '2', '1', '+', '×', '0', '÷']), "NaN")
    
    def test_cf_compute(self):
        '''
         * 测试计算算式的值
        '''
        cf = ComputeFormular()
        self.assertEqual(cf.compute('+', '29', '0'), '29')
        self.assertEqual(cf.compute('-', '19', '0'), '-19')
        self.assertEqual(cf.compute('×', '99', '0'), '0')
        self.assertEqual(cf.compute('÷', '9', '0'), '0')
        self.assertEqual(cf.compute('÷', '0', '9'), 'NaN')
        self.assertEqual(cf.compute('÷', '0', '0'), 'NaN')
        self.assertEqual(cf.compute('+', '1/4', '3/8'), '5/8')
        

if __name__ == "__main__":
    unittest.main()