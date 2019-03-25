import numpy as np
from multiprocessing import Pool
import cv2
from tqdm import tqdm
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

    ######## ifiot prrofing ###############
    if buf_size % 2 == 0:
        buf_size -= 1

    if buf_size == 0:
        buf_size = 50

    frame_width = int(np.shape(video)[2])
    frame_height = int(np.shape(video)[1])

    # print("width: " + str(frame_width))
    # print("height: " + str(frame_height))

    # buffer used for calculating the median
    buf = np.zeros((buf_size, frame_height, frame_width, 3), np.uint8)
    # one frame of background
    bg_frame = np.zeros((frame_height, frame_width, 3), np.uint8)

    # background videoeo to be returned
    output = []

    print("vid len = " + str(len(video)))
    for i in tqdm(range(0, len(video))):

        # if i % 50 is 0:
        #     print("BG generation frame: " + str(i))


        # add the frame to the front of the buffer
        buf[0] = video[i]

        # rotate buffer by 1 position to move the latest frame to the end of the buffer
        buf = np.roll(buf, 1, axis=0)

        # calculate median of buffer and store it in bg_frame maintaing the same data type (uint8)
        bg_frame = bg_frame.copy()
        np.median(buf, axis=0, out=bg_frame)

        # skip the first half of the frames, because media will be black
        if i >= buf_size - 1:
            output.append(bg_frame)

    print(np.shape(output))
    return output


def calc_median(data):
    """
    The parallelized function which calculates median for a specific frame

    Args: a dictionary with video, buf_size, start_index
    """

    video = data["video"]
    buf_size = data["buf_size"]
    start_index = data["start_index"]

    # get a section of the frames from input video
    buffer = video[start_index : start_index + buf_size]

    frame_width = int(np.shape(video)[2])
    frame_height = int(np.shape(video)[1])

    # one frame of background of uint8 data type
    bg_frame = np.zeros((frame_height, frame_width, 3), np.uint8)

    # calculate median on this section
    np.median(buffer, axis=0, out=bg_frame)

    return bg_frame


def create_background_parallel(video, buf_size):
    """
    Creates the background of clip using temporal median - but parallely

    Args:
        video: Input videoeo from which background is to be created; a list of frames
        buf_size: number of frames over which the median is considered;
            Use odd number only;
            higher buffer size -> smoother background

    Returns: List of frames; frame is a 2D numpy array
    """

    # format our input with video, buf_size and start_index as parameters
    # create an empty list
    data = []

    # number of BG frames to be genrated
    num_bg_frames = len(video) - buf_size + 1

    for i in range(0, num_bg_frames):

        data_dict = {
            "video": video,
            "buf_size": buf_size,
            "start_index": i
        }

        data.append(data_dict)

    # data has been created!


    # multiprocessing pool
    pool = Pool(8)
    bg_frames = pool.map(calc_median, data)
    pool.close()
    pool.join()

    print(np.shape(bg_frames))

    return bg_frames
