"""
    Creating annotations for image patches
    Airbus Oil Tank dataset
"""

import os
import json
import random
from pathlib import Path
from PIL import Image
from src.cfg import airbus_clean_otd 

import logging
from logging import config
config.fileConfig('logger.ini')
logger = logging.getLogger(__name__)

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

class dataset_to_coco(airbus_clean_otd):
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
    
    def __init__(self, airbus_dataset_path: str = None) -> None:
        super().__init__(airbus_dataset_path)
        super().annots_pd()
        self.clean_labels = super().clean_annots()

    def dataset_to_coco(
            self,
            image_patch_folder:str = None)-> None:
        """Function to create JSON annotations for image patches
        
            Args:
                image_patch_folder: Image patch folder
        """
        # Building basic annotation JSON dict
        coco_annots_str = ['info', 'licenses', 'categories']
        coco_annots = [info, license, classes]
        for i in range(len(coco_annots)):
            self.annotations_json[coco_annots_str[i]].append(coco_annots[i])
        
        image_patches = os.listdir(image_patch_folder)
        random_patch = random.choice(image_patches)
        image_path = os.path.join(image_patch_folder,random_patch)
        img = Image.open(image_path)
        TILE_HEIGHT, TILE_WIDTH = img.size

        for i in range(len(image_patches)):
        # Add image to annotations JSON
            image = {
                "id": i, 
                "license": 1, 
                "file_name": str(os.path.join(image_patch_folder,image_patches[i])), 
                "height": TILE_HEIGHT,
                "width": TILE_WIDTH, 
                "date_captured": ""
            }        
            self.annotations_json["images"].append(image)

            patch_name = image_patches[i].split('.')[0]
            image_id, x_start, y_start = patch_name.split('_')
            img_labels = self.clean_labels[self.clean_labels["image_id"] == image_id]
            # Getting the bounds
            # Get annotations in tiles
            found_ann = [self.annot_is_inside_tile(bounds, int(x_start), int(y_start), TILE_WIDTH, TILE_HEIGHT, TRUNCATED_PERCENT) for i, bounds in enumerate(img_labels['bounds'])]  
            found_ann = [el for el in found_ann if el is not None]
            # Add annotations to annotations JSON
            # format: 0, x_min, y_min, b_width, b_height
            for ann in found_ann:
                ann_nb = 0
                class_id, x_min, y_min, b_width, b_height = ann
                image_annotations = {
                    "id": ann_nb,
                    "image_id": i,
                    "category_id": class_id,
                    "bbox": [x_min, y_min, b_width, b_height],
                    "area": b_width * b_height,
                    "segmentation": [],
                    "iscrowd": 0
                }
                self.annotations_json["annotations"].append(image_annotations)
                ann_nb += 1 

        # save annotations in JSON file
        parent_dir = Path(image_patch_folder).parents[0].as_posix()
        set_name = image_patch_folder.split('/')[-1]
        annots_json_path = os.path.join("data/splits", f"{set_name}_annots.json")
        with open(annots_json_path, 'w') as f:
            output_json = json.dumps(self.annotations_json)
            f.write(output_json)
        logger.info((f"{len(self.annotations_json['images'])} tiles saved under {parent_dir} as {set_name}_annots.json"))                   



if __name__ == "__main__":
    sets = ["train", "test", "valid"]
    airbus_dataset_path = os.environ.get('AIRBUS_SPOT')
    airbus_image_patches = os.path.join(airbus_dataset_path, 'image_patches')

    for i in sets:
        image_patch_folder = os.path.join(airbus_image_patches, i)
        coco = dataset_to_coco(airbus_dataset_path)
        coco.dataset_to_coco(image_patch_folder)

