import cv2
import cv2.aruco as aruco
import numpy as np
import pickle
# LOAD CAMERA CALIBRATION
with open('output/calibration_data.pkl', 'rb') as f:
    data = pickle.load(f)
camera_matrix = data['camera_matrix']
dist_coeffs = data['distortion_coefficients']
# ARUCO SETTINGS
MARKER_SIZE = 10.0  # cm
aruco_dict = aruco.getPredefinedDictionary(
    aruco.DICT_4X4_50)
detector_params = aruco.DetectorParameters()
# CAMERA
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = aruco.detectMarkers(
        gray,
        aruco_dict,
        parameters=detector_params)
    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners, ids)
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(
            corners,
            MARKER_SIZE,
            camera_matrix,
            dist_coeffs)
        for i in range(len(ids)):
            rvec = rvecs[i]
            tvec = tvecs[i][0]
        # Draw coordinate axes
            cv2.drawFrameAxes(
                frame,
                camera_matrix,
                dist_coeffs,
                rvec,
                tvec,
                MARKER_SIZE)
            x = tvec[0]
            y = tvec[1]
            z = tvec[2]
        # Euclidean distance
            distance = np.sqrt(
                x*x + y*y + z*z)
            cv2.putText(
                frame,
                f"Distance: {distance:.2f} cm",
                (10, 40 + i*30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,0),
                2)
            print(
                f"ID={ids[i][0]} "
                f"X={x:.2f}cm "
                f"Y={y:.2f}cm "
                f"Z={z:.2f}cm "
                f"Dist={distance:.2f}cm")
    cv2.imshow("ArUco Distance", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
