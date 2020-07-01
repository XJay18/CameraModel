import argparse

from config import *
from calibration.calibrate import detect_corners, calibrate, undistort


def arg_parser():
    parser = argparse.ArgumentParser(
        description="Run single camera calibration."
    )
    parser.add_argument(
        "-p", "--path", type=str,
        default=LT_IMG_PATH,
        help="Specify the directory where the images are stored."
    )
    parser.add_argument(
        "-t", "--target", type=str,
        default=LT_UDIMG_PATH,
        help="Specify the directory where the undistorted images will be stored.\n"
             "Note that only the flag '-u','--undistort' is set will the images be saved."
    )
    parser.add_argument(
        "-s", "--show", dest="show",
        action="store_true",
        help="Whether to show chessboard corners when calibrating."
    )
    parser.add_argument(
        "-u", "--undistort", dest="undist",
        action="store_true",
        help="Whether to run the undistort function to undistort the images."
    )
    parser.set_defaults(image=False, undist=False)
    return parser.parse_args()


if __name__ == '__main__':
    arg = arg_parser()

    real_p, img_p, img_shape = detect_corners(arg.path, ld(arg.path), show=True)
    _, mtx, dist, rvector, tvector = calibrate(real_p, img_p, img_shape)
    print("Intrinsic Matrix: \n", mtx)
    print("Distortion Parameters: \n", dist)
    print("Rotation Vectors: \n", rvector)
    print("Translation Vectors: \n", tvector)

    if arg.undist:
        undistort(arg.path, arg.target, ld(arg.path), mtx, dist)
