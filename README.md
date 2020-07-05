### Camera Model
This project gradually designs a pipeline to estimate the depth with cameras. It also provides functions for camera calibration, rectification and so on.

----

### Usage
**Catalogue**
1. [Single Camera Calibration](#scc)
1. [Stereo Camera Calibration](#sc)
1. [Stereo Matching](#sm)

Clone the repository to your machine.
```bash
git clone https://github.com/XJay18/CameraModel.git
```

Enter the main directory
```bash
cd CameraModel/
```

#### <span id="scc">Single Camera Calibration</span>
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
By default, this script will use the images stored at `data/left` to calibrate the camera.

#### <span id="sc">Stereo Camera Calibration</span>
Stereo camera calibration uses images captured from two different cameras to calibrate the two cameras and get the transformation from the first camera's coordinates to the second one. To use this utility, you can run `stereo_cal.py` as following:

```bash
python stereo_cal.py [-h] [-lp LEFT_PATH] [-rp RIGHT_PATH] [-lt LEFT_TARGET]
                     [-rt RIGHT_TARGET] [-ct CHECKED_TARGET] [-r] [-s] [-c]
```
The details of the command line arguments are:
```
optional arguments:
  -h, --help            show this help message and exit
  -lp LEFT_PATH, --left_path LEFT_PATH
                        Specify the directory where the images of left camera
                        are stored.
  -rp RIGHT_PATH, --right_path RIGHT_PATH
                        Specify the directory where the images of right camera
                        are stored.
  -lt LEFT_TARGET, --left_target LEFT_TARGET
                        Specify the directory where the rectified images of
                        left camera will be stored. Note that only the flag
                        '-r','--rectified' is set will the images be saved.
  -rt RIGHT_TARGET, --right_target RIGHT_TARGET
                        Specify the directory where the rectified images of
                        right camera will be stored. Note that only the flag
                        '-r','--rectified' is set will the images be saved.
  -ct CHECKED_TARGET, --checked_target CHECKED_TARGET
                        Specify the directory where the rectified images in
                        pair will be stored. Note that only the flag '-r','--
                        rectified' and '-c','--check' are set will the images
                        be saved.
  -r, --rectified       Whether to run the rectify function to rectify the
                        images.
  -s, --show            Whether to show the rectified images. Note that only
                        the flag '-r','--rectified' is set will the images be
                        shown.
  -c, --check           Whether to visualize the results of rectified images
                        in pair.
```
By default, this script will use the images stored at `data/left` and `data/right` to calibrate the cameras.

#### <span id="sm">Stereo Matching</span>
TODO