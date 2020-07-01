import cv2
import numpy as np

from config import *

CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
W = 9
H = 6


def detect_corners(root_path, files, criteria=CRITERIA, show=False):
    real = np.zeros((W * H, 3), np.float32)
    real[:, :2] = np.mgrid[0:W, 0:H].T.reshape(-1, 2)

    real_points = list()
    img_points = list()
    size = None

    for img in files:
        frame = cv2.imread(os.path.join(root_path, img))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if size is None:
            size = gray.shape[::-1]
        retval, corners = cv2.findChessboardCorners(gray, (W, H))
        if retval:
            cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            real_points.append(real)
            img_points.append(corners)
            if show:
                cv2.drawChessboardCorners(frame, (W, H), corners, retval)
                cv2.imshow("Corners", frame)
                cv2.waitKey(0)
    return real_points, img_points, size


def calibrate(real_points, img_points, size, compute_loss=True):
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(real_points, img_points, size, None, None)
    if compute_loss:
        loss, avg = calibrate_loss(real_points, img_points, rvecs, tvecs, mtx, dist)
        print("Total Error: %.6f" % loss, " | Avg Error: %.6f" % avg)
    # return calibrate results, intrinsics, distortion factor,
    # rotation vectors, and translation vectors
    return ret, mtx, dist, rvecs, tvecs


def calibrate_loss(real_points, img_points, rvecs, tvecs, mtx, dist):
    total_error = 0
    for i in range(len(real_points)):
        imgp, _ = cv2.projectPoints(real_points[i], rvecs[i], tvecs[i], mtx, dist)
        total_error += cv2.norm(img_points[i], imgp, cv2.NORM_L2) / len(imgp)
    return total_error, total_error / len(real_points)


def undistort(source_path, target_path, files, mtx, dist):
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    print("Saving undistorted images to directory: %s..." % target_path)
    for img in files:
        frame = cv2.imread(os.path.join(source_path, img))
        h, w = frame.shape[:2]
        new_camera_mtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 0, (w, h))
        out = cv2.undistort(frame, mtx, dist, None, new_camera_mtx)
        cv2.imwrite(os.path.join(target_path, img), out)
    print("Done")

