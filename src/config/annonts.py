"""
    Cleaning Airbus Oil tank dataset
    
    To check the Kaggle data card of the Airbus Oil tank dataset,
    Open the following link
    https://www.kaggle.com/datasets/airbusgeo/airbus-oil-storage-detection-dataset
    
"""
import os
import ast
import numpy as np
import pandas as pd

import logging
from logging import config
config.fileConfig('logger.ini')
logger = logging.getLogger(__name__)

class airbus_clean_otd:
    """Functions to clean airbus data"""
    @staticmethod
    # convert a string record into a valid python object
    def f(x): 
        return ast.literal_eval(x.rstrip('\r\n'))
    
    @staticmethod
    def getWidth(bounds):
        try: 
            (xmin, ymin, xmax, ymax) = bounds
            return np.abs(xmax - xmin)
        except:
            return np.nan
    
    @staticmethod
    def getHeight(bounds):
        try: 
            (xmin, ymin, xmax, ymax) = bounds
            return np.abs(ymax - ymin)
        except:
            return np.nan 

    def __init__(
            self,
            airbus_dataset_path:str = None) -> None:
        """
            Args:
                airbus_dataset_path: Unzipped path to the airbus dataset
        """
        self.airbus_dataset_path = airbus_dataset_path
        self.annots_path = os.path.join(self.airbus_dataset_path, 'annotations.csv')
        self.labels = pd.read_csv(self.annots_path, converters={'bounds': self.f})

    def annots_pd(self):
        # Create width and height
        self.labels.loc[:,'width'] = self.labels.loc[:,'bounds'].apply(self.getWidth)
        self.labels.loc[:,'height'] = self.labels.loc[:,'bounds'].apply(self.getHeight)
        self.labels.at[:,'aspect_ratio'] = self.labels[['height', 'width']].max(axis=1) / self.labels[['height', 'width']].min(axis=1)
        logger.info("Descriotion o the lables are as follows:")
        logger.info(f'{self.labels.describe()}')
        return self.labels

        self.analysis = '''
        The analysis of the data provides some insights. 
        Bounding boxes are mostly squares with a mean size of 23 pixels i.e. 35 meters. 
        Some aspect ratios are strange either too small or too big. 
        We want to clean this by removing bounding boxes 
        that are too small (height or width under 5 pixels) or with large aspect ratio (over 2.5).  
        '''
        logger.info(f'{self.analysis}')
    
    def clean_annots(self)-> None:
        # parameters to clean data
        keep_tags_wt_width_over_px = 5
        keep_tags_wt_height_over_px = 5
        bb_aspect_ratio_upper_limit =  2.5
        
        # remove null values
        safe_labels = self.labels[(np.isfinite(self.labels['aspect_ratio'])) & self.labels['aspect_ratio'].notnull()]

        # remove very small pixels
        filter_too_small = np.logical_or(safe_labels['width'] < keep_tags_wt_width_over_px, safe_labels['height'] < keep_tags_wt_width_over_px)
        logger.info(f"Removed {sum(filter_too_small)}, records which are too small.")

        # remove weird aspect ratio
        filter_ratio_too_high = safe_labels['aspect_ratio'] > bb_aspect_ratio_upper_limit
        logger.info(f"Removed {sum(filter_ratio_too_high)}, records which have a unusual aspect ratio.")

        cleaned_labels = safe_labels[np.logical_not(np.logical_or(filter_too_small,filter_ratio_too_high))]

        # inspect the values
        logger.info("After cleaning the labels are as follows")
        logger.info(f"{cleaned_labels.describe()}")  
        return cleaned_labels   