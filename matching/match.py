#############################
# Reference
# https://github.com/opencv/opencv/blob/master/samples/python/stereo_match.py
# https://www.cnblogs.com/zhiyishou/p/5767592.html
#############################

import cv2
import numpy as np

from config import *
from calibration.calibrate import detect_corners
from calibration.stereo_calibrate import stereo_calibrate
from calibration.rectification import rectify

ply_header = '''
ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''


def write_ply(fn, verts, colors):
    verts = verts.reshape(-1, 3)
    colors = colors.reshape(-1, 3)
    verts = np.hstack([verts, colors])
    with open(fn, 'wb') as f:
        f.write((ply_header % dict(vert_num=len(verts))).encode('utf-8'))
        np.savetxt(f, verts, fmt='%f %f %f %d %d %d ')


# print the coordinate of the point you clicked
def callbackFunc(e, x, y, f, p):
    if e == cv2.EVENT_LBUTTONDOWN:
        print(p[y][x])


def match(arg):
    if arg.save:
        if not os.path.exists(arg.ply_target):
            os.makedirs(arg.ply_target)
        if not os.path.exists(arg.disparity_target):
            os.makedirs(arg.disparity_target)
        print("==> 'ply' files will be saved in %s." % arg.ply_target)
        print("==> Disparity images will be saved in %s.\n" % arg.disparity_target)

    real_p, img_p1, img_shape = detect_corners(arg.left_path, ld(arg.left_path), show=False)
    _, img_p2, _ = detect_corners(arg.right_path, ld(arg.right_path), show=False)
    _, mtx1, dist1, mtx2, dist2, rot, trans, ess, fund = \
        stereo_calibrate(real_p, img_p1, img_p2, img_shape)

    Q = rectify(mtx1, dist1, mtx2, dist2, img_shape, rot, trans)[4]

    for img1, img2 in zip(ld(arg.left_rect), ld(arg.right_rect)):
        cv2.namedWindow("Disparity")

        print("Loading images ...")
        # read images from disk
        frame1 = cv2.imread(os.path.join(arg.left_rect, img1))
        frame2 = cv2.imread(os.path.join(arg.right_rect, img2))
        # convert into gray images
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        # disparity range is tuned for '05','07','08','13' image pairs
        window_size = 7
        min_disp = 16
        num_disp = 320 - min_disp
        stereo = cv2.StereoSGBM_create(
            minDisparity=min_disp,
            numDisparities=num_disp,
            blockSize=window_size,
            P1=8 * 3 * window_size ** 2,
            P2=32 * 3 * window_size ** 2,
            disp12MaxDiff=200,
            uniquenessRatio=1,
            speckleWindowSize=3,
            speckleRange=1
        )

        print("Computing disparity ...")
        disp = stereo.compute(frame1, frame2).astype(np.float32) / 16.0

        print("Generating 3d point cloud ...")
        print("You can click on the 'Disparity' plane to see "
              "the coordinate of the specific point in terminal.")
        points = cv2.reprojectImageTo3D(disp, Q)
        colors = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        mask = disp > disp.min()
        out_points = points[mask]
        out_colors = colors[mask]

        cv2.setMouseCallback("Disparity", callbackFunc, points)
        cv2.imshow("%s" % img1, frame1)
        cv2.imshow("Disparity", (disp - min_disp) / num_disp)
        if arg.save:
            name1, _ = os.path.splitext(img1)
            name2, _ = os.path.splitext(img2)
            out_fn = os.path.join(arg.ply_target, name1 + "_" + name2 + '.ply')
            write_ply(out_fn, out_points, out_colors)
            print("PLY file saved.")
            cv2.imwrite(os.path.join(arg.disparity_target, name1 + "_" + name2 + ".jpg"), disp)
            print(cv2.imread(os.path.join(arg.disparity_target, name1 + "_" + name2 + ".jpg")))
            print("Disparity image saved.")
        key = cv2.waitKey(0)
        print("Done for pair %s and %s.\n" % (img1, img2))
        cv2.destroyAllWindows()

        # quit if 'Q' or 'q' is pressed
        if key == 81 or key == 113:
            break
