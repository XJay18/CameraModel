import cv2

from calibration.calibrate import calibrate, calibrate_loss


def stereo_calibrate(real_points, img_p1, img_p2, size, compute_loss=True):
    _, mtx1, dist1, rvec1, tvec1 = calibrate(real_points, img_p1, size, compute_loss)
    _, mtx2, dist2, rvec2, tvec2 = calibrate(real_points, img_p2, size, compute_loss)
    ret, mtx1, dist1, mtx2, dist2, rot, trans, ess, fund = \
        cv2.stereoCalibrate(
            real_points, img_p1, img_p2,
            # mtx1, dist1, mtx2, dist2, size, cv2.CALIB_FIX_INTRINSIC)
            mtx1, dist1, mtx2, dist2, size)
    if compute_loss:
        loss1, avg1 = calibrate_loss(real_points, img_p1, rvec1, tvec1, mtx1, dist1)
        loss2, avg2 = calibrate_loss(real_points, img_p2, rvec2, tvec2, mtx2, dist2)
        print("After stereo calibration")
        print("Camera 1 ==> Total Error: %.6f" % loss1, " | Avg Error: %.6f" % avg1)
        print("Camera 2 ==> Total Error: %.6f" % loss2, " | Avg Error: %.6f" % avg2)
    return ret, mtx1, dist1, mtx2, dist2, rot, trans, ess, fund


