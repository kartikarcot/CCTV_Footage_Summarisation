import numpy as np
import cv2

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

def open_video(filename):
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



try:
    cap, frame_width, frame_height = open_video('fgmask.avi')
except IOError as error:
    print(error)
    print('Check the filename or camera.')

volume = [np.zeros((frame_height, frame_width), dtype=np.uint8)] # 3D volume; A list for storing the labelled images
labels = [[1]] # A list storing the tube labels in each image in the volume
tube_num = 0 # Number of tubes found
prev_count = 1 # OpenCV returns at least 1 label (i.e. the background)

overwrite_dict = {}

out = cv2.VideoWriter('debug.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                        15, (frame_width,frame_height))

while(cap.isOpened()):
    ret, frame = cap.read() # Read the frame

    if ret is False: # Frame is read properly
        break

    # Fix JPEG compression issues
    frame[frame>50] = 255
    frame[frame!=255] = 0

    # Find connected components in the current image
    cur_count, cur_img = cv2.connectedComponents(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), connectivity=8)

    ###############################################################
    # Debug output of connected components
    if cur_count > 1:

        cur_img = cur_img.astype(np.uint8)

        label_hue = np.uint8(179*cur_img/np.max(cur_img))
        blank_ch = 255*np.ones_like(label_hue)
        labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
        labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
        labeled_img[label_hue==0] = 0

        cv2.imshow('label', labeled_img)
        out.write(labeled_img)
    ###############################################################

    ret, match_dict = intersecting_regions(cur_img, cur_count, volume[-1], labels[-1])

    cur_label = []

    cur_img_output = cur_img.copy()

    if ret is True:
        # Some current region is intersecting with multiple previous regions

        cur_img_copy = cur_img.copy()

        # Erode the image to try and separate the regions
        kernel = np.ones((5,5), np.uint8)
        cur_img_copy = cv2.erode(cur_img_copy, kernel, iterations = 1)

        cur_count_copy, cur_img_copy = cv2.connectedComponents(cur_img_copy, connectivity=8)

        # Find the number of intersections using eroded image
        ret, match_dict_copy = intersecting_regions(cur_img_copy, cur_count_copy, volume[-1], labels[-1])


        print("intersection " + str(ret) + str(match_dict_copy))

        if ret is False:
            print("erosion success")
            # The intersecting regions have been separated by erosion
            # Replace the image by the eroded image
            cur_img = cur_img_copy
            cur_count = cur_count_copy
            match_dict = match_dict_copy
        else:
            # The intersecting regions did not separate
            # Overwrite matching labels in the volume with current label

            tube_num += 1

            for region in match_dict:
                if len(match_dict[region]) > 1:

                    for index in match_dict[region]:
                        for frame in volume:
                            # Update labels of tubes in previous frame
#                             frame[frame == index] = tube_num
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

    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break

# Update previous frames
# print(overwrite_dict)
for index in overwrite_dict:
    for frame in volume:
        # Update labels of tubes in previous frame
        frame[frame == index] = tube_num

cap.release()
out.release()
cv2.destroyAllWindows()
print('done')
