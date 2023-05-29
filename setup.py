from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'YOLO -Oil Tank Detection'
LONG_DESCRIPTION = """

Modular implementation of Workflow of Oil tank detection - YOLOX
https://www.kaggle.com/code/jeffaudi/oil-storage-detection-on-airbus-imagery-with-yolox

"""

# Setting up
setup(
        name="oiltankYOLO", 
        version=VERSION,
        author="Vardhan Raj Modi",
        author_email="vardhan609@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages()
)