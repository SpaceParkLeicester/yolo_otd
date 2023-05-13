"""
    Creating annotations for image patches
    Airbus Oil Tank dataset
"""

import os
from pathlib import Path
import random
from PIL import Image

info = {
    "year": "2021", 
    "version": "1", 
    "description": "Airbus Oil Storage Detection Dataset - COCO format", 
    "contributor": "Airbus DS GEO S.A.", 
    "url": "https://www.kaggle.com/datasets/airbusgeo/airbus-oil-storage-detection-dataset", 
    "date_created": ""
    }

license = {
    "id": 1,
    "url": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
    "name": "CC BY-NC-SA 4.0"
    }

classes = {
    "id": 0, 
    "name": "oil-storage-tank", 
    "supercategory": "none"
    }

TRUNCATED_PERCENT = 0.3

class dataset_to_coco:
    """Creating annotations in COCO format"""
    annotations_json = {"info": [],"licenses": [], "categories": [],"images": [],"annotations": []} 

    @staticmethod
    # Return one tuple for each tag found inside the tile
    def annot_is_inside_tile(bounds, x_start, y_start, width, height, truncated_percent):
        x_min, y_min, x_max, y_max = bounds
        x_min, y_min, x_max, y_max = x_min - x_start, y_min - y_start, x_max - x_start, y_max - y_start

        if (x_min > width) or (x_max < 0.0) or (y_min > height) or (y_max < 0.0):
            return None
        
        x_max_trunc = min(x_max, width) 
        x_min_trunc = max(x_min, 0) 
        if (x_max_trunc - x_min_trunc) / (x_max - x_min) < truncated_percent:
            return None

        y_max_trunc = min(y_max, width) 
        y_min_trunc = max(y_min, 0) 
        if (y_max_trunc - y_min_trunc) / (y_max - y_min) < truncated_percent:
            return None
        
        return (0, x_min_trunc, y_min_trunc, x_max_trunc - x_min_trunc, y_max_trunc - y_min_trunc)
    
    def __init__(self) -> None:
        pass

    def dataset_to_coco(
            self,
            image_patch_folder:str = None)-> None:
        """Function to create JSON annotations for image patches
        
            Args:
                image_patch_folder: Image patch folder
        """
        # Building basic annotation JSON dict
        coco_annots_str = ['info', 'license', 'classes']
        coco_annots = [info, license, classes]
        for i in range(coco_annots):
            self.annotations_json[coco_annots_str[i]].append(coco_annots[i])
        
        image_patches = os.listdir(image_patch_folder)
        random_patch = random.choice(image_patches)
        img = Image.open(random_patch)
        TILE_HEIGHT, TILE_WIDTH = img.size

        for patch in image_patches:
            patch_name = Path(patch).stem
            image_id, x_start, y_start = patch_name.split('_')
            # Get annotations in tiles
            found_ann = [
                self.annot_is_inside_tile(bounds, x_start, y_start, TILE_WIDTH, TILE_HEIGHT, TRUNCATED_PERCENT)]            



