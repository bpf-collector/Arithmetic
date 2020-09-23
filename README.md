# Arithmetic

小学四则运算题目生成(Generation of arithmetic questions for primary school)

---

## 1. 项目要求

### 1.1 要求概述

> + 生成小学四则运算题目，且结果不出现负数
> + 除了整数外，还要支持真分数的四则运算

### 1.2 项目要求

> [易知大学](http://yz.yzhiliao.com/course/55/task/326/show)

## 2. 解题思路

> + 使用`argparse`库`设置参数`
> + 通过随机数生成`操作数`和`操作符`，通过参数设置操作数个数和操作符种类，再`拼接成算式`
> + 通过随机数生成随机位置，在算式的基础上`插入括号`
> + 通过随机数生成随机位置，将算式的特定数字`替换为分数`

## 3. version 1.0

### 3.1 完成时间: `2020-9-20`

### 3.2 博客地址

> [博客园](https://www.cnblogs.com/bpf-1024/p/13703047.html)

### 3.2 优点

> + 能够包含整数、分数、括号进行运算
> + 进入界面相对美观

### 3.3 缺点

> + 结果可能出现负数，需要改进
> + 题目输出界面不美观
> + 后缀表达式的值计算方法不够简洁，需要改进
