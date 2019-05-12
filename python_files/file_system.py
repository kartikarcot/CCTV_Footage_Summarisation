# import libraries
import numpy as np
import cv2

def open_file(filename):
    """
    Open a video file using VideoCapture object

    Args:
        filename: The name of the file to be opened
            Pass 0 to open webcam, or -1 to search for cameras

    Raises:
        IOError: If the file or stream cannot be opened

    Returns: VideoCapture object, frame width, frame hight
    """

    cap = cv2.VideoCapture(filename) # Init VideoCapture object

    frame_width = frame_height = 0

    # Check if camera opened successfully
    if cap.isOpened() is False:
        raise IOError('Error opening video stream or file.')
    else:
        # Default resolutions of the frame are obtained.
        # We convert the resolutions from float to integer.
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))

    return cap, frame_width, frame_height

def read_file(filename, video=[]):
    """
    Reads a video file

    Args: filename, video - a list of frames (optional)

    Returns: a list of frames; frames are 2D numpy arrays
    """

    # open input video using videoCapture
    try:
        cap, frame_width, frame_height = open_file(filename)
    except IOError as error:
        print(error)
        print('Check the filename or camera.')

    while True:
        ret, frame = cap.read()

        # frame was read properly, not end of file
        if ret is True:
            video.append(frame)
        else:
            break

    return video

def get_video_length(filename):
    """
    Returns the video length of a specified file

    Args: filename

    Returns: num_frames
    """
    # open input video using videoCapture
    try:
        cap, frame_width, frame_height = open_file(filename)
    except IOError as error:
        print(error)
        print('Check the filename or camera.')

    num_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    return num_frames


def read_frame(cap):
    """
    Reads the next frame

    Args: file capture object

    Returns: a frame; frames are 2D numpy arrays,
    """

    # read specific frame
    # cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number-1)
    res, frame = cap.read()

    if res == True:
        return frame
    else:
        print("Error reading frame")


def write_file(video, filename):
    """
        Writes an output file

        Args: video to be written; List of frames

        Returns: nothing
    """
    frame_width = int(np.shape(video)[2])
    frame_height = int(np.shape(video)[1])

    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))
    for frame in video:

        if len(np.shape(frame)) == 2:
            # if image is single channel grayscale, convert it to color
            out.write(cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR))
        else:
            out.write(frame)

    out.release()