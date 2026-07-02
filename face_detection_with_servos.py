import cv2 as cv
import serial
import time
# SERIAL
arduino = serial.Serial('/dev/ttyACM0', 115200)
time.sleep(2)
# CAMERA
cap = cv.VideoCapture(1)
FRAME_W = 640
FRAME_H = 480
cap.set(3, FRAME_W)
cap.set(4, FRAME_H)
CENTER_X = FRAME_W // 2
CENTER_Y = FRAME_H // 2
# FACE DETECTOR
face_cascade = cv.CascadeClassifier(
    cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
# DEADZONE
DEADZONE =15
# PID VALUES
Kp = 0.002 #0.002
Ki = 0.0001 #0.0001
Kd = 0.02 #0.02
# SERVO POSITIONS
servoX = 90
servoY = 90
# PID VARIABLES
prev_error_x = 0
prev_error_y = 0

integral_x = 0
integral_y = 0

prev_time = time.time()

# MAIN LOOP
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv.flip(frame, 1)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
# FACE DETECTION
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=4,
        minSize=(50, 50))
# CENTER BOX
    cv.rectangle(
        frame,
        (CENTER_X - DEADZONE, CENTER_Y - DEADZONE),
        (CENTER_X + DEADZONE, CENTER_Y + DEADZONE),
        (0, 255, 0),
        2)
    if len(faces) > 0:
# Largest face
        largest = max(faces, key=lambda rect: rect[2] * rect[3])
        x, y, w, h = largest

        cx = x + w // 2
        cy = y + h // 2
# DRAW FACE
        cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
# PID
        current_time = time.time()
        dt = current_time - prev_time
# Avoid divide by zero
        if dt == 0:
            dt = 0.01
        error_x = CENTER_X - cx
        error_y = CENTER_Y - cy
# DEADZONE
        if abs(error_x) < DEADZONE:
            error_x = 0
        if abs(error_y) < DEADZONE:
            error_y = 0
# INTEGRAL
        integral_x += error_x * dt
        integral_y += error_y * dt
# DERIVATIVE
        derivative_x = (error_x - prev_error_x) / dt
        derivative_y = (error_y - prev_error_y) / dt
# PID OUTPUT
        output_x = (
            Kp * error_x +
            Ki * integral_x +
            Kd * derivative_x)
        output_y = (
            Kp * error_y +
            Ki * integral_y +
            Kd * derivative_y)
# SERVO UPDATE
        servoX -= output_x
        servoY -= output_y
# LIMITS
        servoX = max(0, min(180, servoX))
        servoY = max(0, min(180, servoY))
# SEND TO ARDUINO
        data = f"{int(servoX)},{int(servoY)}\n"
        arduino.write(data.encode())
# SAVE VALUES
        prev_error_x = error_x
        prev_error_y = error_y
        prev_time = current_time
# DISPLAY INFO
        posX = int(servoX)
        posY = int(servoY)
        cv.putText(frame,f"X:{posX} Y:{posY}",(10, 30),cv.FONT_HERSHEY_SIMPLEX,1,(0, 255, 0),2)
# RETURN SERVO
    else:
        if servoX > 90:
            servoX -= 1
        elif servoX < 90:
            servoX += 1

        if servoY > 90:
            servoY -= 1
        elif servoY < 90:
            servoY += 1

        # SEND UPDATED POSITION
        data = f"{int(servoX)},{int(servoY)}\n"
        arduino.write(data.encode())
# SHOW
    cv.imshow("Face Tracking", frame)
    key = cv.waitKey(1)
    if key == 27:
        break
cap.release()
cv.destroyAllWindows()
arduino.close()
