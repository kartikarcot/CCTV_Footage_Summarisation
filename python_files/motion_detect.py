import numpy as np
import cv2

# open input video
cap = cv2.VideoCapture('TestVid1.mp4')

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# create video writer object to create output video
out = cv2.VideoWriter('fgmask.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 15, (frame_width,frame_height))

# create background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True, history=100)

# kernel for morphological operations
kernel1 = np.ones((3,3),np.uint8)
kernel2 = np.ones((9,9),np.uint8)

threshold = frame_width * frame_height / 200
print(threshold)

while(1):
    # read the frame
    ret, frame = cap.read()
    
    if ret is True:

        # apply the mask to the blurred frame
        fgmask = fgbg.apply(frame)
        
        # remove shadow
        fgmask[fgmask != 255] = 0
        
        cv2.imshow("fg", fgmask)
        
        # apply blur to remove noise
#         blur = cv2.GaussianBlur(fgmask, (5,5), 0)
        
#         cv2.imshow("blur", blur)
        
        # remove small noise
        img = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel1)
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel1)
        
        
        img = cv2.dilate(img,kernel2,iterations = 1)
        
        ########### COOOL
        
        
        count, img = cv2.connectedComponents(img, connectivity=8)
        
        unique, count = np.unique(img, return_counts=True)
        for i in range(0, len(count)):
            if count[i] < threshold:
                img[img == unique[i]] = 0
                
        img[img != 0] = 255
        
        img = img.astype(np.uint8)
        
        ############## END COOOL
        
        cv2.imshow("coool", img)
        
        colorImg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        out.write(colorImg)
            
        k = cv2.waitKey(3) & 0xff
        if k == 27:
            break
    else:
        break
    
cap.release()
out.release()

cv2.destroyAllWindows()