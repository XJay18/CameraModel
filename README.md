### Camera Model
This project gradually designs a pipeline to estimate the depth with cameras. It also provides functions for camera calibration, rectification and so on.

----

### Usage

Clone the repository to your machine.
```bash
git clone https://github.com/XJay18/CameraModel.git
```

Enter the main directory
```bash
cd CameraModel/
```

#### Single Camera Calibration
Single camera calibration uses images captured from one camera to calibrate the camera (i.e., to get the intrinsics and extrinsics of the camera). To use this utility, you can run `single_cal.py` as following:
```bash
python single_cal.py [-h] [-p PATH] [-t TARGET] [-s] [-u]
```
The details of the command line arguments are:
```
optional arguments:
-h, --help            show this help message and exit
-p PATH, --path PATH  Specify the directory where the images are stored.
-t TARGET, --target TARGET
                        Specify the directory where the undistorted images
                        will be stored. Note that only the flag '-u','--
                        undistort' is set will the images be saved.
-s, --show            Whether to show chessboard corners when calibrating.
-u, --undistort       Whether to run the undistort function to undistort the
                        images.
```
By default, this script will use the images stored at `data/left_undistort` to calibrate the camera.

#### Stereo Camera Calibration
