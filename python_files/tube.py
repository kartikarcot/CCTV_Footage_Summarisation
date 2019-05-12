import numpy as np
import cv2
import file_system as fs
import random


class Tube(object):
    """
    A tube object contains all the parameters and volumes associated with an event aka tube

    Attributes:
        object_tube: list of frames [4 dimensional]; Only the detected object is masked out
        mask_tube: list of frames [3 dimensional]; The B&W mask of the detected object
        start: actual start frame of the tube
        end: actual end frame of the tube
        length: length of the tube (given by end-start)
    """
    def __init__(self, object_tube = [], mask_tube = [], start = 0, end = 0, length = 0):
            self.object_tube = object_tube
            self.mask_tube = mask_tube
            self.start = start
            self.end = end
            self.length = length
            self.tags = None

            return

    def create_object_tube(self, video):
        """
        Creates a color object tube of the object by applying the mask_tube
        onto the original input video

        Args:
            video: list of frames (3 channel); the original input video
        """

        self.object_tube = []

        for i in range(0, self.length):

            # mask has to be converted to 3 channel for bitwise operation
            mask_3c = cv2.cvtColor(self.mask_tube[i], cv2.COLOR_GRAY2BGR)
            video_frame = video[self.start + i]

            # use 'bitwise and' operation to apply the object mask onto the input video
            color_frame = cv2.bitwise_and(video_frame, mask_3c)
            self.object_tube.append(color_frame)

        # fs.write_file(self.object_tube, "../debug/objecttube" + str(random.randint(1,100)) + ".avi")

        return


def binary_mask(img, val, replacement_val):
    """
    Create a binary mask of the image

    Args:
        img: An image to be masked
        val: The value in the image to be masked
        replacement_val: The high value to be used in the binary mask

    Returns: Nothing. Masking is performed in-place.
    """

    img[img != val] = 0 # Pixels not equal to the required value are made 0
    img[img == val] = replacement_val # Pixels equal to the required value are set to replacement value
    return

def intersecting_regions(cur_img, cur_count, prev_img, prev_labels,
                        intersection_threshold = 0.2):

    """
    Find the number of intersecting regions between the any region in the
    current image and any regions in the previous image

    Args:
        cur_img: The labelled image of the current frame returned by OpenCV
            Connected Components

        cur_count: Number of components in cur_img

        prev_img: The labelled image of the previous frame returned by OpenCV
            Connected Components

        prev_labels: The tube labels present in the prev_img

        intersection_threshold: Fraction of intersection between regions in
        previous and current image

    Returns: A dict mapping intersecting regions in current frame to regions in
        the previous frame
            Example:
                {
                    2 : [2, 3],
                    3 : [4]
                }
    """


    # Create a copy of the images to prevent overwriting the parameters
    prev_img = prev_img.copy()
    cur_img = cur_img.copy()

    match_dict = {} # Dictionary to store the intersecting regions

    # Stores whether any current region intersect with multiple previous regions
    multiple_intersections = False

    for region_cur in range(1, cur_count):

        # Create a copy of the image for this iteration
        cur_img_copy = cur_img.copy()
        binary_mask(cur_img_copy, region_cur, 1)

        matches = [] # Clear matches list for each region in current image

        for region_prev in prev_labels:

            # Create a copy of the image for this iteration
            prev_img_copy = prev_img.copy()
            binary_mask(prev_img_copy, region_prev, 1)

            # Multiply masks to find the intersections of regions
            intersection = prev_img_copy * cur_img_copy

            # Number of intersecting pixels
            intersection_count = np.sum(intersection)

            # Number of pixels in previous region
            region_prev_count = np.sum(prev_img_copy)

            # Region is matched if intersection fraction greater than threshold
            if intersection_count/region_prev_count > intersection_threshold:
                matches.append(region_prev)

        if len(matches) > 1:
            multiple_intersections = True

        match_dict[region_cur] = matches

    return multiple_intersections, match_dict

def extract_tubes(labelled_volume):
    """
    Extracts mask tubes of each event from a single labelled volume

    Args:
        labelled_volume: list of frames;
            In each frame, pixel value = 0 represents BG,
            while non-zero pixel values represent the corresponding event

    Returns:
        A list of Tube objects with the mask tube extracted,
        start frame, end frame and length attributes set
    """

    # threshold of active pixels for tubes to be extracted
    THRESHOLD = 10000

    tubes = [] # list of tube objects

    # get the unique labels within the volume
    uniq, count = np.unique(labelled_volume, return_counts = True)

    # skip label 0, since it represents the BG (OpenCV connected components output)
    for i in range(1, len(uniq)):

        # skip tubes where the active pixel count is less, it is probably noise
        if count[i] < THRESHOLD:
            print("Skipped " + str(count[i]))
            continue

        # Create a new tube object
        tube = Tube()
        tube.mask_tube = []

        curr_label = uniq[i] # current label

        # set the start and end of this tube to be start and end of video
        start_extraction = False
        tube.start = 0
        tube.end = len(labelled_volume)

        # iterate through frames and set actual start & end point
        for frame_no, frame in enumerate(labelled_volume):
            if (not start_extraction and frame[frame==curr_label].any()):
                start_extraction = True
                tube.start = frame_no
            if (start_extraction and not frame[frame==curr_label].any()):
                tube.end = frame_no
                tube.length = tube.end - tube.start
                break

            if start_extraction is True:
                # we require a new frame
                frame_copy = frame.copy()
                frame_copy[frame_copy==curr_label] = 255
                frame_copy[frame_copy!=255] = 0
                frame_copy = frame_copy.astype(np.uint8)  # make sure type is uint8
                tube.mask_tube.append(frame_copy)

        tubes.append(tube)
        # fs.write_file(tube.mask_tube, "../debug/masktube" + str(random.randint(1,100)) + ".avi")

    return tubes

def label_tubes(video_mask):
    """
    Detects and labels the tubes aka events in the masked video

    Args:
        video_mask: a list of frames (single channel)

    Returns: labelled video
    """

    frame_width = int(np.shape(video_mask)[2])
    frame_height = int(np.shape(video_mask)[1])

    # 3D volume; A list of frames storing the labelled images
    # Added a blank frame so that there is a 'previous frame' for the first frame of input
    volume = [np.zeros((frame_height, frame_width), dtype=np.uint8)]
    labels = [[1]] # A list storing the tube labels in each image in the volume
    tube_num = 0 # Number of tubes found
    prev_count = 1 # OpenCV returns at least 1 label (i.e. the background)

    overwrite_dict = {}

    for i in range(0, len(video_mask)):

        frame = video_mask[i]

        # Find connected components in the current image
        cur_count, cur_img = cv2.connectedComponents(frame, connectivity=8)

        ###############################################################
        # Debug output of connected components
        if cur_count > 1:

            cur_img = cur_img.astype(np.uint8)

            label_hue = np.uint8(179*cur_img/np.max(cur_img))
            blank_ch = 255*np.ones_like(label_hue)
            labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
            labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
            labeled_img[label_hue==0] = 0

            # cv2.imshow('label', labeled_img)
            # out.write(labeled_img)
        ###############################################################

        ret, match_dict = intersecting_regions(cur_img, cur_count, volume[-1], labels[-1])

        cur_label = []

        cur_img_output = cur_img.copy()

        if ret is True:
            # There are intersecting regions
            # Overwrite matching labels in the volume with current label
            tube_num += 1

            for region in match_dict:
                if len(match_dict[region]) > 1:

                    for index in match_dict[region]:
                        for frame in volume:
                            # Update labels of tubes in previous frame
                            frame[frame == index] = tube_num
                            # Add an entry to the overwrite dict
                            overwrite_dict[index] = [tube_num]

                    # Update the dict
                    match_dict[region] = [tube_num]
#                     cur_img[cur_img == region] = tube_num
#                     cur_label.append(tube_num)

        # There are no intersection issues; Proceed normally
        for region in match_dict:
            if len(match_dict[region]) == 0:
                # New region found since there is no match to any previous region
                tube_num += 1
                cur_img_output[cur_img == region] = tube_num
                cur_label.append(tube_num)

            else:
                # Some previous region was found, relabel the region
                cur_img_output[cur_img == region] = match_dict[region][0]
                cur_label.append(match_dict[region][0])


        volume.append(cur_img_output)
    #     print(cur_label)
        labels.append(cur_label) # Convert keys in the match_dict to a list of labels of current image
        prev_count = cur_count

    # Update previous frames
    # print(overwrite_dict)
    # for index in overwrite_dict:
    #     for frame in volume:
    #         # Update labels of tubes in previous frame
    #         frame[frame == index] = tube_num

    # Remove the 1st blank frame added in the beginning
    del volume[0]

    return volume

