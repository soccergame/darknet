#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 作者：何智翔
# 描述：训练数据预处理
# 创建日期：20181012

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
    u'[2]商品数据/VOC2007new/labels/')

label_txt = 'material_onlyone.names'

image_dir = (
    u'E:/工作资料/[2]图像部门/[4]图像数据/' + 
    u'[2]商品数据/VOC2007new/JPEGImages_original/')

show_label_result_dir = (
    u'E:/工作资料/[2]图像部门/[4]图像数据/' + 
    u'[2]商品数据/VOC2007new/JPEGImages_with_other/')

image_names = os.listdir(image_dir)

with open(os.path.join(label_dir, label_txt)) as infile:
    id2name = infile.readlines()
    infile.close()

for image_name in image_names:
    if '.jpg' not in image_name:
        continue

    image = image_read(os.path.join(image_dir, image_name))
    resized_size = 416
    image_size = max(image.shape[0], image.shape[1])
    scale_ratio = resized_size / image_size
    image = cv2.resize(image, None, fx=scale_ratio, fy=scale_ratio)
    resized_height = image.shape[0]
    resized_width = image.shape[1]
    
    shift_height = (resized_size - resized_height) // 2
    shift_width = (resized_size - resized_width) // 2
    resized_image = np.zeros((resized_size, resized_size, 3), dtype=np.uint8)
    resized_image[
      shift_height:(shift_height + resized_height), 
      shift_width:(shift_width + resized_width), 
      :] = image[:,:,:]

    label_name = image_name.replace('.jpg', '.txt')

    if os.path.exists(os.path.join(label_dir, label_name)):
        with open(os.path.join(label_dir, label_name), 'r') as infile:
            labels = infile.readlines(False)
            infile.close()

        new_labels = []
        for label in labels:
            label = label.rstrip().split(' ')
            #if 'other' not in id2name[int(label[0])]:
            #    continue

            x = int(float(label[1]) * resized_size)
            y = int(float(label[2]) * resized_size)
            w = int(float(label[3]) * resized_size)
            h = int(float(label[4]) * resized_size)

            left = int(x + 1 - 0.5 * w)# + shift_width
            top = int(y + 1 - 0.5 * h)# + shift_height
            right = int(x + 1 + 0.5 * w)# + shift_width
            bottom = int(y + 1 + 0.5 * h)# + shift_height

            #x = (left + right)/2.0 - 1
            #y = (top + bottom)/2.0 - 1
            #w = right - left
            #h = bottom - top

            #new_label = '{0} {1} {2} {3} {4}'.format(
            #    label[0], x / resized_size, y / resized_size, 
            #    w / resized_size, h / resized_size)
            #new_labels.append(new_label)
            #thickness = max(
            #    2, int(0.005 * float(
            #        min(resized_image.shape[0], resized_image.shape[1])) 
            #           + 0.5))
            ##font_scale = 0.5 / 540.0 * float(min(image.shape[0], image.shape[1]))
            #cv2.rectangle(resized_image, (left, top), 
            #              (right, bottom), (255, 0, 255), 
            #              thickness)
            #cv2.putText(image, id2name[int(label[0])].rstrip(), (left, top - 5), 
            #            cv2.FONT_HERSHEY_SIMPLEX,
            #            font_scale / 4, (255, 0, 255), 1)

        #with open(os.path.join(label_dir, label_name), 'w') as outfile:
        #    for new_label in new_labels:
        #        outfile.write('{}\n'.format(new_label))
        #    outfile.close()

        image_write(os.path.join(show_label_result_dir, image_name), resized_image)
    else:
        print(u'标定文件{}不存在\n'.format(label_name))