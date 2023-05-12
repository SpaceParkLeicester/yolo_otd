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
        return self.labels
    
    def clean