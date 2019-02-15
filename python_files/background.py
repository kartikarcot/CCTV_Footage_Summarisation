import numpy as np
import cv2

cap = cv2.VideoCapture('DubRun.mp4')

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

bufCap = 41

# record the video
# out1 = cv2.VideoWriter('original.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 15, (frame_width,frame_height))
out2 = cv2.VideoWriter('DubBG.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 15, (frame_width,frame_height))

buf = np.zeros((bufCap, frame_height, frame_width, 3),np.uint8)
bg = np.zeros((frame_height, frame_width, 3),np.uint8)

while(1):
    # read the frame
    ret, frame = cap.read()
    
    if ret is True:
        
        # convert to greyscale
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # add frame to buffer
        buf[0] = frame
        
#         cv2.imshow('frame0', buf[0])
        
        # rotate buffer by 1 position to move the latest frame to the end of the buffer
        buf = np.roll(buf, 1, axis=0)
#         print(np.shape(buf))
        np.median(buf, axis=0, out=bg)
#         bg = cv2.cvtColor(bg, cv2.COLOR_GRAY2BGR)
        
        # write original frame
#         out1.write(frame)
        # write calculated background frame
        sum = np.sum(bg)
        if sum > 0:
            out2.write(bg)
            cv2.imshow('bg', bg)
        
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
    else:
        break
    
cap.release()
# out1.release()
out2.release()

cv2.destroyAllWindows()