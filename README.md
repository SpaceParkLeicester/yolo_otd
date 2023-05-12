# YOLO-Airbus Oil tank detection

(Kaggle Notebook)[https://www.kaggle.com/code/jeffaudi/oil-storage-detection-on-airbus-imagery-with-yolox/notebook]

### Installation - Requirements

Note: Both CUDA-10.1 and CUDA-10.2 should be added to `/usr/local/`, and add below line to the `.bashrc`
```
export LD_LIBRARY_PATH=/usr/local/cuda-10.2/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
```

Make sure to run `environment.yml` to install all necessary packages, and the (YOLOX detection)[https://github.com/Megvii-BaseDetection/YOLOX] is adapted  from the given link, make sure to clone the repo and install it as ediatable. 