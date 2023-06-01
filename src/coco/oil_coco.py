"""
    Add a class called 'oil' in pre-defined coco class
"""

import os
from string import Template

coco_cls = '''
COCO_CLASSES = (
  "oil",
)
'''

config_file_template = '''
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (c) Megvii, Inc. and its affiliates.

import os
from yolox.exp import Exp as MyExp

class Exp(MyExp):
    def __init__(self):
        super(Exp, self).__init__()
        self.depth = 0.33
        self.width = 0.50
        self.input_size = (640, 640)
        self.test_size = (640, 640)
        self.exp_name = os.path.split(
            os.path.realpath(__file__))[1].split(".")[0]
        self.enable_mixup = False
        self.multiscale_range = 0
        
        # Define yourself dataset path
        self.data_dir = "$data_dir"
        self.train_ann = "$train_ann"
        self.val_ann = "$valid_ann"
        self.test_ann = "$test_ann"

        self.max_epoch = $max_epoch
        self.num_classes = 1
        #self.data_num_workers = 2      
        self.eval_interval = 1
        
        self.flip_prob = 0.5
        #self.no_aug_epochs = 2
'''
PIPELINE_CONFIG_PATH = 'src/config.py'

def add_oil_to_coco(yolox_install_path:str = None):
    """
        Add where the YOLOX repo has been downloaded and installed as editable.
    """
    coco_class_path = 'YOLOX/yolox/data/datasets/coco_classes.py'
    coco_class_path = os.path.join(yolox_install_path, coco_class_path)
    with open(coco_class_path, 'w') as f:
        f.write(coco_cls)
    
    pipeline = Template(config_file_template).substitute(
        data_dir = os.getcwd(),
        train_ann = os.path.join(os.getcwd(), 'data/splits/train_annots.json'),
        valid_ann = os.path.join(os.getcwd(), 'data/splits/valid_annots.json'),
        test_ann = os.path.join(os.getcwd(), 'data/splits/test_annots.json'),
        max_epoch = 10)
    with open(PIPELINE_CONFIG_PATH, 'w') as f:
        f.write(pipeline)

if __name__ == "__main__":
    yolox_install_path = os.environ.get('YOLOX')
    add_oil_to_coco(yolox_install_path)
