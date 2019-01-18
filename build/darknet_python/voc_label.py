#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 作者：何智翔
# 描述：修改以读取我们自己的VOC格式文件用于训练
# 创建日期：20180930
# ==============================================================================

import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

#sets=[('2012', 'train'), ('2012', 'val'), ('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

#classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

classes = []

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(xml_path, label_path):
    in_file = open(xml_path)
    out_file = open(label_path, 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        #if 'other' in cls:
        #    continue
        cls = 'SKU'

        if cls not in classes or int(difficult)==1:
            classes.append(cls)
            cls_id = len(classes) - 1
        else:
            cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    out_file.close()
    in_file.close()

# wd = getcwd()

if __name__ == "__main__":
    # 读取所有的xml文件
    annotation_path = (
        u'E:/工作资料/[2]图像部门/[4]图像数据/' + 
        u'[2]商品数据/VOC2007new/Annotations_update/')

    xml_paths = os.listdir(annotation_path)

    for xml_path in xml_paths:
        if 'xml' not in xml_path:
            continue

        # 转换xml文件到yolo能够识别的格式
        txt_path = xml_path.replace('xml', 'txt')
        convert_annotation(os.path.join(annotation_path, xml_path), 
                           os.path.join(annotation_path, txt_path))

    sku_id_path = 'voc.names'
    out_file = open(os.path.join(annotation_path, sku_id_path), 'w')
    for class_name in classes:
        out_file.write('{}\n'.format(class_name))
    out_file.close()


        
#for year, image_set in sets:
#    if not os.path.exists('VOCdevkit/VOC%s/labels/'%(year)):
#        os.makedirs('VOCdevkit/VOC%s/labels/'%(year))
#    image_ids = open('VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()
#    list_file = open('%s_%s.txt'%(year, image_set), 'w')
#    for image_id in image_ids:
#        list_file.write('%s/VOCdevkit/VOC%s/JPEGImages/%s.jpg\n'%(wd, year, image_id))
#        convert_annotation(year, image_id)
#    list_file.close()

#os.system("cat 2007_train.txt 2007_val.txt 2012_train.txt 2012_val.txt > train.txt")
#os.system("cat 2007_train.txt 2007_val.txt 2007_test.txt 2012_train.txt 2012_val.txt > train.all.txt")