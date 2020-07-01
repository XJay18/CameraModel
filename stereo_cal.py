import argparse

from config import *
from calibration.calibrate import detect_corners
from calibration.stereo_calibrate import stereo_calibrate
from calibration.rectification import rectify, remap, check_rectification


def arg_parser():
    parser = argparse.ArgumentParser(
        description="Run stereo camera calibration."
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
        "-lt", "--left_target", type=str,
        default=LT_RIMG_PATH,
        help="Specify the directory where the rectified images of left camera will be stored.\n"
             "Note that only the flag '-r','--rectified' is set will the images be saved."
    )
    parser.add_argument(
        "-rt", "--right_target", type=str,
        default=RT_RIMG_PATH,
        help="Specify the directory where the rectified images of right camera will be stored.\n"
             "Note that only the flag '-r','--rectified' is set will the images be saved."
    )
    parser.add_argument(
        "-ct", "--checked_target", type=str,
        default=CHECK_RECT,
        help="Specify the directory where the rectified images in pair will be stored.\n"
             "Note that only the flag '-r','--rectified' and '-c','--check' are set "
             "will the images be saved."
    )
    parser.add_argument(
        "-r", "--rectified", dest="rect",
        action="store_true",
        help="Whether to run the rectify function to rectify the images."
    )
    parser.add_argument(
        "-s", "--show", dest="show",
        action="store_true",
        help="Whether to show the rectified images.\n"
             "Note that only the flag '-r','--rectified' is set will the images be shown."
    )
    parser.add_argument(
        "-c", "--check", dest="check",
        action="store_true",
        help="Whether to visualize the results of rectified images in pair."
    )
    parser.set_defaults(rect=False, show=False, check=False)
    return parser.parse_args()


if __name__ == '__main__':
    arg = arg_parser()

    # stereo calibration
    real_p, img_p1, img_shape = detect_corners(arg.left_path, ld(arg.left_path), show=False)
    _, img_p2, _ = detect_corners(arg.right_path, ld(arg.right_path), show=False)
    _, mtx1, dist1, mtx2, dist2, rot, trans, ess, fund = \
        stereo_calibrate(real_p, img_p1, img_p2, img_shape)
    print("Rotation Matrix: \n", rot)
    print("Translation Matrix Parameters: \n", trans)
    print("Essential Matrix: \n", ess)
    print("Fundamental Matrix: \n", fund)

    # rectification
    if arg.rect:
        map11, map12, map21, map22, _, _, _ = rectify(mtx1, dist1, mtx2, dist2, img_shape, rot, trans)
        remap(arg.left_path, arg.left_target, ld(arg.left_path), map11, map12, show=arg.show)
        remap(arg.right_path, arg.right_target, ld(arg.right_path), map21, map22, show=arg.show)

        # check rectification result
        if arg.check:
            check_rectification(
                arg.left_target, ld(arg.left_target),
                arg.right_target, ld(arg.right_target), arg.checked_target)
