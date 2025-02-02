# import cv2
# import numpy as np
# import api.api as api

# criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# objp = np.zeros((6 * 9, 3), np.float32)
# objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)

# # Arrays to store object points and image points from all the images.
# objpoints = []  # 3d point in real world space
# imgpoints = []  # 2d points in image plane.

# # Acquisisci 15 frame della scacchiera
# for _ in range(15):
#     rgb = api.get_rgb()
#     gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
#     ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)
#     if ret:
#         cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
#         objpoints.append(objp)
#         imgpoints.append(corners)

# # Calcola parametri intrinseci
# ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
#     objpoints, imgpoints, gray.shape[::-1], None, None
# )
# print("Focal Length (fx, fy):", mtx[0, 0], mtx[1, 1])
# print("Optical Center (cx, cy):", mtx[0, 2], mtx[1, 2])
