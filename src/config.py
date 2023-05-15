
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
        self.data_dir = "/home/vardh/gcp_projects/airbus-ml"
        self.train_ann = "/home/vardh/gcp_projects/airbus-ml/data/train_annots.json"
        self.val_ann = "/home/vardh/gcp_projects/airbus-ml/data/valid_annots.json"
        self.test_ann = "/home/vardh/gcp_projects/airbus-ml/data/test_annots.json"

        self.max_epoch = 10
        self.num_classes = 1
        #self.data_num_workers = 2      
        self.eval_interval = 1
        
        self.flip_prob = 0.5
        #self.no_aug_epochs = 2
