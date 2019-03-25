import numpy as np
import cv2

def extract_tubes(labelled_volume):
    """
    Extracts each tube into individual volumes
    """

    tubes = [] # list of volumes

    # get the unique labels within the volume
    uniq = np.unique(labelled_volume)

    # skip index 0, since it is BG
    for i in range(1, len(uniq)):

        tube = []   # tube of current object

        label = uniq[i] # current label

        for frame in labelled_volume:
            frame_copy = frame.copy()
            frame_copy[frame_copy==label] = 255
            frame_copy[frame_copy!=255] = 0
            frame_copy = frame_copy.astype(np.uint8)  # make sure type is uint8
            tube.append(frame_copy)

        tubes.append(tube)

    return tubes


