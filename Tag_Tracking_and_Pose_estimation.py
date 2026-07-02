import cv2
import cv2.aruco as aruco
import numpy as np
import pickle
import serial
import time
# PID CLASS
class PID:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0
        self.prev_error = 0
    def update(self, error):
        self.integral += error
        derivative = error - self.prev_error
        output = (
            self.kp * error +
            self.ki * self.integral +
            self.kd * derivative)
        self.prev_error = error
        return output
# SERIAL
arduino = serial.Serial('/dev/ttyACM0', 115200)
time.sleep(2)
# LOAD CALIBRATION
with open("output/calibration_data.pkl", "rb") as f:
    data = pickle.load(f)
camera_matrix = data["camera_matrix"]
dist_coeffs = data["distortion_coefficients"]
# ARUCO
MARKER_SIZE = 10.0  # cm
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
params = aruco.DetectorParameters()
# CAMERA
cap = cv2.VideoCapture(0)
# PID PARAMETERS
pan_pid = PID(
    kp=1.0, # 0.3 default
    ki=0.0, # default 0.01 or 0.009
    kd=0.1) # 0.0 default
tilt_pid = PID(
    kp=1.0,
    ki=0.0,
    kd=0.1)
# SERVO SETTINGS
CENTER_PAN = 90
CENTER_TILT = 90
pan_angle = 90
tilt_angle = 90
DEADZONE = 0.0      # cm
RETURN_SPEED = 1.5  # deg/frame 1.5 default
# LOOP
while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = aruco.detectMarkers(gray,aruco_dict,parameters=params)
# MARKER DETECTED
    if ids is not None:
        aruco.drawDetectedMarkers(frame,corners,ids)
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(
            corners,
            MARKER_SIZE,
            camera_matrix,
            dist_coeffs)
        tvec = tvecs[0][0]
        x = tvec[0]
        y = tvec[1]
        z = tvec[2]
        cv2.drawFrameAxes(
            frame,
            camera_matrix,
            dist_coeffs,
            rvecs[0],
            tvecs[0],
            MARKER_SIZE)
# CENTER CONDITION
        if abs(x) < DEADZONE:
            pan_angle = CENTER_PAN
        else:
            correction = pan_pid.update(x)
            pan_angle = CENTER_PAN - correction
        if abs(y) < DEADZONE:
            tilt_angle = CENTER_TILT
        else:
            correction = tilt_pid.update(y)
            tilt_angle = CENTER_TILT + correction
# MARKER LOST
    else:
        if pan_angle > CENTER_PAN:
            pan_angle -= RETURN_SPEED
        elif pan_angle < CENTER_PAN:
            pan_angle += RETURN_SPEED
        if tilt_angle > CENTER_TILT:
            tilt_angle -= RETURN_SPEED
        elif tilt_angle < CENTER_TILT:
            tilt_angle += RETURN_SPEED
# LIMITS
    pan_angle = max(0,min(180, pan_angle))
    tilt_angle = max(0,min(180, tilt_angle))
# SEND TO ARDUINO
    message = (
        f"{int(pan_angle)},"
        f"{int(tilt_angle)}\n")
    arduino.write(message.encode())
# DISPLAY
    cv2.putText(
        frame,
        f"PAN : {int(pan_angle)}",
        (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0,255,0),
        2)
    cv2.putText(
        frame,
        f"TILT : {int(tilt_angle)}",
        (10, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0,255,0),
        2)
    if ids is not None:
        cv2.putText(
            frame,
            f"X={x:.1f} cm",
            (10,120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,0,0),
            2)
        cv2.putText(
            frame,
            f"Y={y:.1f} cm",
            (10,160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,0,0),
            2)
        cv2.putText(
            frame,
            f"Z={z:.1f} cm",
            (10,200),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,0,0),
            2)
    cv2.imshow("ArUco PID Tracker",frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
arduino.close()
cv2.destroyAllWindows()
