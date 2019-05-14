import numpy as np
import cv2

class MotionDetect(object):

    def __init__(self):
        self.fgbg = cv2.createBackgroundSubtractorMOG2()
        # kernel for morphological operations
        self.kernel1 = np.ones((3,3),np.uint8)
        self.kernel2 = np.ones((5,5),np.uint8)

    def detect_motion(self, frame):
        """
        Detect motion  and create a FG mask using MOG2

        Args: input frame; 3 channels

        Returns: masked frame (greyscale image, single channel) &
            calculated static background frame,
            is_motion - whether motion is detected in this frame or not
        """
        frame_width = int(np.shape(frame)[1])
        frame_height = int(np.shape(frame)[0])

        # create background subtractor
        # fgbg = cv2.createBackgroundSubtractorMOG2()
        # fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True)




        # apply the mask to the frame
        fgmask = self.fgbg.apply(frame)

        # remove shadow
        fgmask[fgmask != 255] = 0

        # if (np.sum(fgmask)/255 >5000):
        #     cv2.imshow("window0", fgmask)
        #     cv2.waitKey(0)
        #     cv2.destroyAllWindows()

        # remove small noise
        img = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, self.kernel1)
        # img = cv2.morphologyEx(img, cv2.MORPH_OPEN, self.kernel1)

        # if (np.sum(img)/255 >100):
        #     cv2.imshow("window1", img)
        #     cv2.waitKey(0)
        #     cv2.destroyAllWindows()

        # dilate to get larger blob
        img = cv2.dilate(img, self.kernel2, iterations = 1)

        ########### COOOL

        # finds components in the image and suppresses the components
        # which are smaller than the threshold to eliminate small patches
        # print("height is " + str(frame_height))
        # print("width is " + str(frame_width))
        threshold = frame_width * frame_height / 200
        # print("threshold is " + str(threshold))
        count, img = cv2.connectedComponents(img, connectivity=8)

        unique, count = np.unique(img, return_counts=True)
        for i in range(0, len(count)):
            # print(str(unique[i]) + " " + str(count[i]))
            if count[i] < threshold:
                img[img == unique[i]] = 0

        img[img != 0] = 255

        img = img.astype(np.uint8)

        ############## END COOOL

        # if (np.sum(img)/255 >5000):
        #     cv2.imshow("window2", img)

        # dilate to get larger blob
        img = cv2.dilate(img, self.kernel2, iterations = 3)

        # if (np.sum(img)/255 >0):
        #     cv2.imshow("window3", img)
        #     cv2.waitKey(0)
        #     cv2.destroyAllWindows()

        # Get the background image from the model
        bg_img = self.fgbg.getBackgroundImage()

        is_motion = False

        # check if there are any white pixels in the mask
        if (np.sum(img) > 0):
            is_motion = True

        return img, bg_img, is_motion