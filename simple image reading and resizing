import cv2 as cv
image = cv.imread('/home/lakshya/opencv/image_read/raw_image2.webp')
cv.imshow('raw_image', image)
cv.waitKey(0)
def rescaleframe(frame, scale=0.75):
    widht = frame.shape[1]*scale # widht of our image or frame...
    height = frame.shape[0]*scale # height of our image or frame...
    w = int(widht)
    h = int(height)
    dimensions = (w, h)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA) # resize the image to a particular dimension...
resized_image = rescaleframe(image, 0.75)
cv.imshow('resized_image', resized_image)
cv.waitKey(0)
