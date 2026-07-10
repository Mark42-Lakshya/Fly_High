import cv2
cap = cv2.VideoCapture(1)
count = 0
while True:
    ret, frame = cap.read()
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == ord('s'):
        cv2.imwrite(f"calibration_images/calib_{count}.jpg", frame)
        count += 1
        print("Saved")
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
