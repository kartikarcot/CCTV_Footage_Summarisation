import cv2
import numpy as np

# open input video
cap = cv2.VideoCapture(0)

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# create video writer object to create output video

# out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 15, (frame_width,frame_height))

# create background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()

# number of pixels which are not black (aka foreground) for detection
threshold = 1000 * 255


while(1):
    # read the frame
    ret, frame = cap.read()

    if ret is True:
        cv2.imshow('frame',frame)

        #apply blur to remove noise
        # blur = cv2.GaussianBlur(frame, (5,5), 0)

        # apply the mask to the blurred frame
        fgmask = fgbg.apply(frame)

        bg = fgbg.getBackgroundImage()

        cv2.imshow('background', bg)
        # cv2.waitKey(30)

        # # sum of intensity values of all the pixels of the masked image
        # sum = np.sum(fgmask)

        # # this frame has motion
        # if sum > threshold:
        #     # write the frame
        #     # out.write(frame)


        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    else:
        break

cap.release()
# out.release()

cv2.destroyAllWindows()