import numpy as np
import cv2
from random import uniform, random

import database as db
import optimize as op
import blend as bd
import background
import file_system as fs

class VideoSummary(object):

    def __init__(self):
        pass

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

        bg = background.create_timelapse_video(bg, video_length)


        for i, key in enumerate(tube_dict):

            print("summary i = " + str(i))

            # index where the frames have to be put in the background
            copy_index = tube_dict[key][1]
            copy_length = tube_dict[key][2]
            actual_start = tube_dict[key][3]

            # color tube
            tube = tube_dict[key][0]
            masked_tube = masked_tubes[i]
            # index of frame to be copied
            index = 0


            for j in range(copy_index, copy_index+copy_length):
                bg[j] = bd.blend_image(bg[j], tube[index], masked_tube[index])
                # cv2.imshow('bg', bg[j])
                # cv2.imshow('fg', tube[index])
                # cv2.imshow('mask', masked_tubes[i][index])
                # cv2.waitKey(0)

                # Add timestamp
                bg[j] = bd.add_timestamp(bg[j], masked_tube[index], actual_start + index)

                index += 1



        for i in range(0, video_length):
            summary.append(bg[i])

        # cv2.destroyAllWindows()
        return summary



if __name__ == '__main__':

    # filepath = "../videos/"
    filename = '8min1.mp4'
    # url = filepath + filename

    vid_sum = VideoSummary()

    db.create_connection()
    selected_tubes = db.get_tubes_by_query(filename, 0, 15000, ['car', 'person'], 30)
    phase1_iterations = db.get_clip_iterations(filename)

    print("Iterations: " + str(phase1_iterations))

    anneal = op.SimulatedAnnealing(100, 1, 100, 5)
    tube_dict = {}


    total_tube_len = 0
    for i,tube in enumerate(selected_tubes):
        total_tube_len += tube.length

    prev_len = 0
    for i,tube in enumerate(selected_tubes):
        # volume, start time (initialize it to 0), length, actual start time
        # tube_dict[i] = [np.asarray(tube.object_tube), 0, tube.length, tube.start]

        # try random start times within a given bound
        tube_dict[i] = [np.asarray(tube.object_tube), int(uniform(0, 1) * total_tube_len * 0.75), tube.length, tube.start]
        # prev_len = prev_len + len(tube['color_tube'])

        # print(np.shape(tube_dict[i][0]))

    '''
    tube_dict = { 1: [a, 0, 50],
        2: [c, 0, 150],
        3: [b, 0, 50],
    }
    '''
    tube_dict = anneal.run(tube_dict, total_tube_len)
    for i,key in enumerate(tube_dict):
        print(tube_dict[key][1:])

    masked_tubes = []
    for i,tube in enumerate(selected_tubes):
        masked_tubes.append(tube.mask_tube)
        # fs.write_file(tube['tube'], str(i)+'.avi')

    # read BG file
    bg = []
    for i in range(1, phase1_iterations):
        fs.read_file("../storage/background_" + filename + "_" + str(i) + ".avi", bg)

        if i > 8:
            break

    summary = vid_sum.make_summary(tube_dict, bg, masked_tubes)

    fs.write_file(summary, "summary_vid.avi")