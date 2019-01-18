#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 作者：何智翔
# 描述：将训练和测试数据整理成为绝对路径的列表
# 创建日期：20181008


import os

base_dir = 'E:/工作资料/[2]图像部门/[4]图像数据/[2]商品数据/VOC2007new/JPEGImages'
suffix = '.jpg'

txt_path = (
    u'E:/工作资料/[2]图像部门/[4]图像数据/[2]商品数据' + 
    u'/VOC2007new/ImageSets/Main/test.txt')

result_path = (
    u'E:/工作资料/[2]图像部门/[4]图像数据/[2]商品数据' + 
    u'/VOC2007new/ImageSets/Main/test_yolo_windows.txt')

with open(txt_path) as infile:
    names = infile.readlines()
    infile.close()

with open(result_path, 'wb') as outfile:
    for name in names:
        name = name.rstrip()
        whole_path = os.path.join(base_dir, name) + suffix
        whole_path = whole_path.replace('\\', '/')
        outfile.write('{}\n'.format(whole_path).encode('utf-8'))

    outfile.close()
