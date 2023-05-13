import os
import random
from PIL import Image

def airbus_img_dims():
    large_img_folder = '/home/vardh/apps/tmp/airbus/images/'
    images = os.listdir(large_img_folder)
    image = random.choice(images)
    img = Image.open(image)
    return [img.size[0], img.size[1]] # IMAGE_HEIGHT, IMAGE_WIDTH

