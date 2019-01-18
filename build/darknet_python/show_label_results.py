#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 作者：何智翔
# 描述：显示标注的结果
# 创建日期：20180930
# 修改日期：20181008
# 修改日志：创建时候没有写完该代码，今天进行补完
# ==============================================================================

import os
import cv2
import numpy as np

def image_read(image_path):
    image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8),-1)
    return image

def image_write(image_path, image, ext='.jpg'):
    cv2.imencode(ext,image)[1].tofile(image_path)

label_dir = (
    u'E:/工作资料/[2]图像部门/[4]图像数据/' + 
    u'[2]商品数据/VOC2007new/labels_onlyone/')

label_txt = 'voc.names'

image_dir = (
    u'E:/工作资料/[2]图像部门/[4]图像数据/' + 
    u'[2]商品数据/VOC2007new/JPEGImages_with_other/')

show_label_result_dir = (
    u'E:/工作资料/[2]图像部门/[4]图像数据/' + 
    u'[2]商品数据/VOC2007new/show_results/')

image_names = os.listdir(image_dir)

show_result_from_voc = False

if show_result_from_voc == True:
    with open(os.path.join(label_dir, label_txt)) as infile:
        id2name = infile.readlines()
        infile.close()
    
    for image_name in image_names:
        if '.jpg' not in image_name:
            continue
    
        image = image_read(os.path.join(image_dir, image_name))
    
        label_name = image_name.replace('.jpg', '.txt')
    
        if os.path.exists(os.path.join(label_dir, label_name)):
            with open(os.path.join(label_dir, label_name), 'r') as infile:
                labels = infile.readlines(False)
                infile.close()
    
            for label in labels:
                label = label.rstrip().split(' ')
                x = int(float(label[1]) * image.shape[1])
                y = int(float(label[2]) * image.shape[0])
                w = int(float(label[3]) * image.shape[1])
                h = int(float(label[4]) * image.shape[0])
    
                left = int(x + 1 - 0.5 * w)
                top = int(y + 1 - 0.5 * h)
                right = int(x + 1 + 0.5 * w)
                bottom = int(y + 1 + 0.5 * h)
    
                thickness = max(
                    2, int(0.005 * float(min(image.shape[0], image.shape[1])) + 0.5))
                font_scale = 0.5 / 540.0 * float(min(image.shape[0], image.shape[1]))
                cv2.rectangle(image, (left, top), 
                              (right, bottom), (255, 0, 255), 
                              thickness)
                cv2.putText(image, id2name[int(label[0])].rstrip(), (left, top - 5), 
                            cv2.FONT_HERSHEY_SIMPLEX,
                            font_scale / 4, (255, 0, 255), 1)
    
            image_write(os.path.join(show_label_result_dir, image_name), image)
        else:
            print(u'标定文件{}不存在\n'.format(label_name))
else:
    image_names = os.listdir(image_dir)

    for image_name in image_names:
        if '.jpg' not in image_name:
            continue

        image = image_read(os.path.join(image_dir, image_name))

        label_name = image_name.replace('.jpg', '.txt')

        if os.path.exists(os.path.join(label_dir, label_name)):
            with open(os.path.join(label_dir, label_name), 'r') as infile:
                labels = infile.readlines(False)
                infile.close()

            for label in labels:
                label = label.rstrip().split(' ')

                x = int(float(label[1]) * image.shape[1])
                y = int(float(label[2]) * image.shape[0])
                w = int(float(label[3]) * image.shape[1])
                h = int(float(label[4]) * image.shape[0])

                left = int(x + 1 - 0.5 * w)
                top = int(y + 1 - 0.5 * h)
                right = int(x + 1 + 0.5 * w)
                bottom = int(y + 1 + 0.5 * h)

                thickness = max(
                    2, int(0.005 * float(min(image.shape[0], image.shape[1])) + 0.5))
                #font_scale = 0.5 / 540.0 * float(min(image.shape[0], image.shape[1]))
                cv2.rectangle(image, (left, top), 
                              (right, bottom), (255, 0, 255), 
                              thickness)
                #cv2.putText(image, id2name[int(label[0])].rstrip(), (left, top - 5), 
                #            cv2.FONT_HERSHEY_SIMPLEX,
                #            font_scale / 4, (255, 0, 255), 1)

            image_write(os.path.join(show_label_result_dir, image_name), image)
        else:
            print(u'标定文件{}不存在\n'.format(label_name))







