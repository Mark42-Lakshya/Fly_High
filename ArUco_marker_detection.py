import cv2 as cv
import cv2.aruco as aruco

cap = cv.VideoCapture(0)

dictionary = aruco.getPredefinedDictionary(
    aruco.DICT_4X4_50
)

while True:

    isTrue, frame = cap.read()

    corners, ids, rejected = aruco.detectMarkers(
        frame,
        dictionary
    )

    if ids is not None:

        # DRAW MARKERS
        aruco.drawDetectedMarkers(frame, corners, ids)

        # PRINT IDS
        print("Detected IDs:", ids.flatten())

        for i, corner in enumerate(corners):

            pts = corner[0]

            # CENTER OF MARKER
            cx = int(pts[:, 0].mean())
            cy = int(pts[:, 1].mean())

            # DRAW CENTER
            cv.circle(frame, (cx, cy), 5, (0,255,0), -1)

            # SHOW ID TEXT
            cv.putText(
                frame,
                f"ID: {ids[i][0]}",
                (cx - 20, cy - 20),
                cv.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,255,0),
                2
            )

    else:

        cv.putText(
            frame,
            "No Marker Detected",
            (20,40),
            cv.FONT_HERSHEY_SIMPLEX,
            1,
            (0,0,255),
            2
        )

    cv.imshow("Frame", frame)

    if cv.waitKey(1) & 0xFF == ord('p'):
        break

cap.release()
cv.destroyAllWindows()
