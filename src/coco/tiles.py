"""
    YOLOX default input size is 640 * 640 pixels,
    so this class function is used for tiling of large images
"""
import os
import random
import numpy as np
from PIL import Image
from tqdm import tqdm
from typing import List

import logging
from logging import config
config.fileConfig('logger.ini')
logger = logging.getLogger(__name__)

# Create 640 x 640 tiles with 64 pix overlap in /kaggle/working
TILE_WIDTH = 640
TILE_HEIGHT = 640
TILE_OVERLAP = 64
_overwriteFiles = True

ann_nb = 0
img_nb = 0

class tiling_data:
    """Tiling large images into small patches"""
    
    def __init__(
            self,
            image_id_list:List = None,
            large_images_folder:str = None,
            destination_data_path:str = None) -> None:
        """Declaring variables
        
        Args:
            image_id_list: List of image ids, either train, test, val ids
            large_images_folder: Airbus large images folder
            destination_data_path: Destination where the tiles needs to be stored
        """
        self.image_id_list = image_id_list
        self.large_images_folder = large_images_folder
        self.destination_data_path = destination_data_path
    
    def tiling(self)-> None:
        # Getting the dimensions of an image
        random_image = random.choice(self.image_id_list)
        random_img_path = os.path.join(self.large_images_folder, random_image+'.jpg')
        img = Image.open(random_img_path)
        IMAGE_HEIGHT, IMAGE_WIDTH = img.size       

        
        for img_id in tqdm(self.image_id_list):            
            # Open image and related data
            pil_img = Image.open(os.path.join(self.large_images_folder, img_id + '.jpg'), mode='r')
            np_img = np.array(pil_img, dtype=np.uint8)

            # Count number of sections to make
            X_TILES = (IMAGE_WIDTH + TILE_WIDTH - TILE_OVERLAP - 1) // (TILE_WIDTH - TILE_OVERLAP)
            Y_TILES = (IMAGE_HEIGHT + TILE_HEIGHT - TILE_OVERLAP - 1) // (TILE_HEIGHT - TILE_OVERLAP)  

            # Cut each tile
            for x in range(X_TILES):
                for y in range(Y_TILES):

                    x_end = min((x + 1) * TILE_WIDTH - TILE_OVERLAP * (x != 0), IMAGE_WIDTH)
                    x_start = x_end - TILE_WIDTH
                    y_end = min((y + 1) * TILE_HEIGHT - TILE_OVERLAP * (y != 0), IMAGE_HEIGHT)
                    y_start = y_end - TILE_HEIGHT
                    save_tile_path = os.path.join(self.destination_data_path, img_id + "_" + str(x_start) + "_" + str(y_start) + ".jpg") 

                    # Save if file doesn't exit
                    if _overwriteFiles or not os.path.isfile(save_tile_path):
                        cut_tile = np.zeros(shape=(TILE_WIDTH, TILE_HEIGHT, 3), dtype=np.uint8)
                        cut_tile[0:TILE_HEIGHT, 0:TILE_WIDTH, :] = np_img[y_start:y_end, x_start:x_end, :]
                        cut_tile_img = Image.fromarray(cut_tile)
                        cut_tile_img.save(save_tile_path)                                                   

if __name__ == "__main__":
    data = ['train.txt', 'test.txt', 'valid.txt']
    for i in data:
        logger.info(f"Commencing the tiling of {i.split('.')[0]} data")
        file_path = os.path.join('data/splits', i)
        with open(file_path) as file:
            data = file.read().rsplit('\n')
        image_id_list = data[:-1]

        large_image_folder = '/home/vardh/apps/tmp/airbus/images/'
        destination_data_path = f'/home/vardh/apps/tmp/airbus/image_patches/{i.split(".")[0]}'
        if not os.path.isdir(destination_data_path):
            os.makedirs(destination_data_path)
        
        data = tiling_data(image_id_list, large_image_folder, destination_data_path)
        data.tiling()
        logger.info("Tiling finished!")
