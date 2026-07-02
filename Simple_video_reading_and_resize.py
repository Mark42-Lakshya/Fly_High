import cv2 as cv
video = cv.VideoCapture('/home/lakshya/opencv/read_video/raw_video2.mp4')
def rescaleframe(frame,scale=0.75):
    widht = frame.shape[1]*scale
    height = frame.shape[0]*scale
    w = int(widht)
    h = int(height)
    dimensions = (w, h)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)
while True:
    isTrue, frame = video.read()
    resized_frame = rescaleframe(frame, 0.40)
    # cv.imshow('Video', frame) # original framesize...
    cv.imshow('resized_video', resized_frame)
    if cv.waitKey(20) & 0xFF == ord('p'):
        break
video.release()
cv.destroyAllWindows()
