import numpy as np
import cv2

def detect_motion(video):
    """
    Detect motion  and create a FG mask using MOG2

    Args: input video; 3 channels

    Returns: masked video; greyscale image (single channel) &
        calculated static background
    """

    output = []
    bg = []

    frame_width = int(np.shape(video)[2])
    frame_height = int(np.shape(video)[1])

    # create background subtractor
    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True)

    # kernel for morphological operations
    kernel1 = np.ones((3,3),np.uint8)
    kernel2 = np.ones((9,9),np.uint8)

    for i in range(0, len(video)):

        # read the frame
        frame = video[i]

        # apply the mask to the frame
        fgmask = fgbg.apply(frame)

        # remove shadow
        fgmask[fgmask != 255] = 0

        # remove small noise
        img = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel1)
        # img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel1)

        # dilate to get larger blob
        img = cv2.dilate(img,kernel2,iterations = 1)

        ########### COOOL

        # finds components in the image and suppresses the components
        # which are smaller than the threshold to eliminate small patches

        threshold = frame_width * frame_height / 200

        count, img = cv2.connectedComponents(img, connectivity=8)

        unique, count = np.unique(img, return_counts=True)
        for i in range(0, len(count)):
            if count[i] < threshold:
                img[img == unique[i]] = 0

        img[img != 0] = 255

        img = img.astype(np.uint8)

        ############## END COOOL

        output.append(img)

        # Get the background image from the model
        bg_img = fgbg.getBackgroundImage()
        bg.append(bg_img)

    return output, bg