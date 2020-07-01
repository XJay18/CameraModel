import os
import cv2
import numpy as np


def rectify(mtx1, dist1, mtx2, dist2, size, rot, trans):
    rot1, rot2, p1, p2, q, roi1, roi2 = cv2.stereoRectify(mtx1, dist1, mtx2, dist2, size, rot, trans)
    map11, map12 = cv2.initUndistortRectifyMap(mtx1, dist1, rot1, p1, size, cv2.CV_32FC1)
    map21, map22 = cv2.initUndistortRectifyMap(mtx2, dist2, rot2, p2, size, cv2.CV_32FC1)
    return map11, map12, map21, map22, q, roi1, roi2


def remap(source_path, target_path, files, map1, map2, show=False):
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    print("Saving rectified images to directory: %s..." % target_path)
    for img in files:
        frame = cv2.imread(os.path.join(source_path, img))
        rect = cv2.remap(frame, map1, map2, cv2.INTER_LINEAR)
        if show:
            cv2.imshow("Rectified Image", rect)
            cv2.waitKey(0)
        cv2.imwrite(os.path.join(target_path, img), rect)
    print("Done")


def check_rectification(path1, files1, path2, files2, target_path=None):
    if target_path is not None and not os.path.exists(target_path):
        os.makedirs(target_path)
    for img1, img2 in zip(files1, files2):
        frame1 = cv2.imread(os.path.join(path1, img1))
        frame2 = cv2.imread(os.path.join(path2, img2))
        total_size = (max(frame1.shape[0], frame2.shape[0]), frame1.shape[1] + frame2.shape[1], 3)
        frame = np.zeros(total_size, dtype=np.uint8)
        frame[:frame1.shape[0], :frame1.shape[1]] = frame1
        frame[:frame2.shape[0], frame1.shape[1]:] = frame2
        for i in range(20, frame.shape[0], 25):
            cv2.line(frame, (0, i), (frame.shape[1], i), (255, 0, 0))
        cv2.imshow('Pair of Rectified Images', frame)
        if target_path is not None:
            name1, _ = os.path.splitext(img1)
            name2, _ = os.path.splitext(img2)
            cv2.imwrite(os.path.join(target_path, name1 + "_" + name2 + ".jpg"), frame)
        cv2.waitKey(0)
