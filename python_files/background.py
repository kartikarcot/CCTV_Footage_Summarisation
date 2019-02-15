import numpy as np
import cv2

def create_background(video, buf_size):
    """
    Creates the background of clip using temporal median

    Args:
        video: Input videoeo from which background is to be created; a list of frames
        buf_size: number of frames over which the median is considered;
            Use odd number only;
            higher buffer size -> smoother background

    Returns: List of frames; frame is a 2D numpy array
    """

    frame_width = int(np.shape(video)[2])
    frame_height = int(np.shape(video)[1])

    print("width: " + str(frame_width))
    print("height: " + str(frame_height))

    # buffer used for calculating the median
    buf = np.zeros((buf_size, frame_height, frame_width, 3), np.uint8)
    # one frame of background
    bg_frame = np.zeros((frame_height, frame_width, 3),np.uint8)

    # background videoeo to be returned
    output = []

    for i in range(0, len(video)):

        # add the frame to the front of the buffer
        buf[0] = video[i]

        # rotate buffer by 1 position to move the latest frame to the end of the buffer
        buf = np.roll(buf, 1, axis=0)

        # calculate median of buffer and store it in bg_frame maintaing the same data type (uint8)
        np.median(buf, axis=0, out=bg_frame)

        # skip the first half of the frames, because media will be black
        if i > buf_size/2:
            output.append(bg_frame)

    return output