import os
import numpy as np
import pandas as pd
from src.cfg import airbus_clean_otd as clean

# Percentage to allocate to train, validation and test datasets
train_ratio = 0.75
valid_ratio = 0.15
test_ratio = 0.10

class test_train_val:
    """Function to create splits in airbus dataset"""
    @staticmethod
    def saveList(sample, filename):
        out_file = open(filename, 'w', encoding='utf-8')
        for c in sample:
            out_file.write(c+'\n')
    
    def __init__(
            self,
            data_dir:str = None,
            cleaned_labels:pd.DataFrame = None) -> None:
        """Declaring variables
        
        Args:
            data_dir: Working data directory to save files
            cleaned_labels: Cleaned labels in pandas format
        """
        self.data_dir = data_dir
        self.cleaned_labels = cleaned_labels
    
    def split(self)-> None:
        if not os.path.isdir(self.data_dir):
            os.makedirs(self.data_dir)
            
            image_ids = self.cleaned_labels.image_id.unique()
            np.random.shuffle(image_ids)

            a = int((1.-valid_ratio-test_ratio)*len(image_ids))
            b = int((1.-test_ratio)*len(image_ids))
            train_ids, valid_ids, test_ids = np.split(image_ids, [a, b])

            self.saveList(train_ids, os.path.join(self.data_dir, 'train.txt'))
            self.saveList(valid_ids, os.path.join(self.data_dir, 'valid.txt'))
            self.saveList(test_ids, os.path.join(self.data_dir, 'test.txt'))

        else:
            # Read splits from previously saved files
            # This enables consistency when running multiple times.
            train_ids = np.loadtxt(os.path.join(self.data_dir, 'train.txt'), dtype=str)
            valid_ids = np.loadtxt(os.path.join(self.data_dir,'valid.txt'), dtype=str)
            test_ids = np.loadtxt(os.path.join(self.data_dir,'test.txt'), dtype=str)        

if __name__ == "__main__":
    airbus_dataset_path = '/home/vardh/apps/tmp/airbus/'
    data_dir = 'data/splits'
    clean_pd= clean(airbus_dataset_path)
    clean_pd.annots_pd()
    cleaned_labels = clean_pd.clean_annots()
    dataset = test_train_val(data_dir,cleaned_labels)
    dataset.split()
