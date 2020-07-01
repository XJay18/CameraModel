import argparse

from config import *
from matching.match import match


def arg_parser():
    parser = argparse.ArgumentParser(
        description="Run stereo matching process."
    )
    parser.add_argument(
        "-lp", "--left_path", type=str,
        default=LT_IMG_PATH,
        help="Specify the directory where the images of left camera are stored."
    )
    parser.add_argument(
        "-rp", "--right_path", type=str,
        default=RT_IMG_PATH,
        help="Specify the directory where the images of right camera are stored."
    )
    parser.add_argument(
        "-lr", "--left_rect", type=str,
        default=LT_RIMG_PATH,
        help="Specify the directory where the rectified images of left camera is stored."
    )
    parser.add_argument(
        "-rr", "--right_rect", type=str,
        default=RT_RIMG_PATH,
        help="Specify the directory where the rectified images of right camera is stored."
    )
    parser.add_argument(
        "-pt", "--ply_target", type=str,
        default=PLY_DIR,
        help="Specify the directory where the ply files will be stored.\n"
             "These .ply files can be viewed in 3D cloud points using MeshLab (http://meshlab.sourceforge.net/)\n"
             "Note that only the flag '-s','--save' is set will the files be saved."
    )
    parser.add_argument(
        "-dt", "--disparity_target", type=str,
        default=DISPARITY_DIR,
        help="Specify the directory where the disparity images will be stored.\n"
             "Note that only the flag '-s','--save' is set will the images be saved."
    )
    parser.add_argument(
        "-s", "--save", dest="save",
        action="store_true",
        help="Whether to save the ply files and disparity images."
    )
    parser.set_defaults(save=False)
    return parser.parse_args()


if __name__ == '__main__':
    arg = arg_parser()
    match(arg)
