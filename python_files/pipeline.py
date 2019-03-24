# import libraries
import numpy as np
import cv2
from timeit import default_timer as timer


# user imports
import background
import motion_detect as md
import tubes as tb
import optimize as op
import blend as bd

class VideoSummary(object):

    def __init__(self):
        pass

    def open_file(self, filename):
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

    def read_file(self, filename):
        """
        Reads a video file

        Args: none

        Returns: a list of frames; frames are 2D numpy arrays
        """

        video = []

        # open input video using videoCapture
        try:
            cap, frame_width, frame_height = self.open_file(filename)
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

    def write_file(self, video, filename):
        """
            Writes an output file

            Args: video to be written; List of frames

            Returns: nothing
        """
        frame_width = int(np.shape(video)[2])
        frame_height = int(np.shape(video)[1])

        out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc('M','J','P','G'), 15, (frame_width,frame_height))
        for frame in video:

            if len(np.shape(frame)) == 2:
                # if image is single channel grayscale, convert it to color
                out.write(cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR))
            else:
                out.write(frame)

        out.release()

    def calc_length(self, tube_dict):
        values = []
        for key in tube_dict:
            values.append(tube_dict[key][1] + tube_dict[key][2])
        return max(values)

    def make_summary(self, tube_dict, bg, masked_tubes):
        """
        make final summary video
        """

        summary = []

        video_length = self.calc_length(tube_dict)

        for i, key in enumerate(tube_dict):

            print("summary i = " + str(i))

            # index where the frames have to be put in the background
            copy_index = tube_dict[key][1]
            copy_length = tube_dict[key][2]

            # color tube
            tube = tube_dict[key][0]

            # index of frame to be copied
            index = 0


            for j in range(copy_index, copy_index+copy_length):
                bg[j] = bd.blend_image(bg[j], tube[index], masked_tubes[i][index])
                cv2.imshow('bg', bg[j])
                cv2.imshow('fg', tube[index])
                cv2.imshow('mask', masked_tubes[i][index])
                cv2.waitKey(0)
                index += 1

        for i in range(0, video_length):
            summary.append(bg[i])

        cv2.destroyAllWindows()
        return summary


if __name__ == '__main__':
    vid_sum = VideoSummary()
    video = vid_sum.read_file('../20sec.mp4')

    # start = timer()
    # bg = background.create_background_parallel(video[0:200], 151)
    # end = timer()
    # print("Parallel: " + str(end - start))

    # start = timer()
    # bg = background.create_background(video[0:200], 151)
    # end = timer()
    # print("Serial: " + str(end - start))

    # vid_sum.write_file(bg, "../20sec_BG_TEST.avi")
    # bg = vid_sum.read_file('../20sec_BG.avi')

    # exit()
    motion_mask = md.detect_motion(video)

    vid_sum.write_file(motion_mask, "motion_mask.avi")

    exit()

    labelled_volume  = tb.label_tubes(motion_mask)
    print("done labelling tubes\n")

    uniq, count = np.unique(labelled_volume, return_counts = True)
    print(uniq)
    print(count)

    tubes = tb.extract_tubes(labelled_volume)
    print("\ndone extracting volumes\n")

    object_tubes, masked_tubes = tb.create_object_tubes(video, tubes)
    print("\ndone creating color and masked tubes")

    # for i in range(0, len(object_tubes)):
    #     vid_sum.write_file(object_tubes[i], "filename{}.avi".format(i))


    anneal = op.SimulatedAnnealing(10000, 1, 20, 3)

    tube_dict = {}

    for i in range(0, len(object_tubes)):
        tube_dict[i] = [np.asarray(object_tubes[i]), 0, len(object_tubes[i])]

    # tube_dict = { 1: [a, 0, 50],
    #     2: [c, 0, 150],
    #     3: [b, 0, 50],
    # }

    tube_dict = anneal.run(tube_dict)

    summary = vid_sum.make_summary(tube_dict, bg, masked_tubes)

    vid_sum.write_file(summary, "summary.avi")