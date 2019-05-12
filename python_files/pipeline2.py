# import libraries
import numpy as np
import cv2
from timeit import default_timer as timer
import skimage.measure
import random

from pympler import muppy, summary

# user imports
import background
import motion_detect as md
import tube as tb
import optimize as op
import blend as bd
import object_detector as od
import file_system as fs
import database as db

SEGMENT_LENGTH = 500

def process_segment(cap, motionDetector, cur_frame, vid_len, completed_iterations, obj_det, filename, clip_tags):

    is_video_processing = True
    is_motion = False
    cur_segment_len = 0

    video = []
    motion_mask = []
    bg = []

    while not(cur_segment_len >= SEGMENT_LENGTH and is_motion is False) and (is_video_processing is True):

        # read more frames
        frame = fs.read_frame(cap)
        cur_segment_len += 1
        cur_frame += 1
        mask_frame, bg_frame, is_motion = motionDetector.detect_motion(frame)

        # print(cur_frame)

        video.append(frame)
        motion_mask.append(mask_frame)
        bg.append(bg_frame)

        if cur_frame == vid_len:
            is_video_processing = False


    # print("\nAfter loading video frames")
    # all_objects = muppy.get_objects()
    # sum1 = summary.summarize(all_objects)
    # summary.print_(sum1)

    print("\nmotion mask length: " + str(len(motion_mask)))
    # fs.write_file(motion_mask, "../debug/motionmask.avi")
    print("Started processing")
    # stop reading frames do the remaining processing

    labelled_volume  = tb.label_tubes(motion_mask)
    print("done labelling tubes")

    # print("\nAfter labelling tubes")
    # all_objects = muppy.get_objects()
    # sum1 = summary.summarize(all_objects)
    # summary.print_(sum1)

    tubes = tb.extract_tubes(labelled_volume)
    print("done extracting tubes")

    # print("\nAfter extracting tubes")
    # all_objects = muppy.get_objects()
    # sum1 = summary.summarize(all_objects)
    # summary.print_(sum1)

    # added color tube into each tube dictionary in the list
    for tube in tubes:
        tube.create_object_tube(video)
        print("done creating color tubes")
        # fs.write_file(tube.object_tube, "../debug/objecttube" + str(random.randint(1,100)) + ".avi")

    # print("\nAfter creating color tubes")
    # all_objects = muppy.get_objects()
    # sum1 = summary.summarize(all_objects)
    # summary.print_(sum1)

    for tube in tubes:
        obj_det.add_tags(tube)

    # print("\nAfter adding tags")
    # all_objects = muppy.get_objects()
    # sum1 = summary.summarize(all_objects)
    # summary.print_(sum1)

    for tube in tubes:
        tube.start = tube.start + completed_iterations * SEGMENT_LENGTH
        tube.end = tube.end + completed_iterations * SEGMENT_LENGTH
        clip_tags = clip_tags.union(set(tube.tags))

    db.create_connection()
    db.save_tubes(tubes, filename)

    # print("\nAfter saving tubes")
    # all_objects = muppy.get_objects()
    # sum1 = summary.summarize(all_objects)
    # summary.print_(sum1)

    # save background
    fs.write_file(bg, "../storage/background_" +
        filename + "_" + str(completed_iterations) + ".avi")

    all_tags = obj_det.get_all_tags(tubes)
    print("all_tags: " + str(all_tags))
    print("cur frame: " + str(cur_frame))

    # reset
    # cur_segment_len = 0

    # for it in range(0, len(video)):
    #     video[it] = None
    #     motion_mask[it] = None
    # # motion_mask = []
    # # video = []
    # tubes = []
    # # bg = []


    # print("After clear:")
    # all_objects = muppy.get_objects()
    # sum1 = summary.summarize(all_objects)
    # summary.print_(sum1)

    # fs.write_file(video, "../debug/video" + str(random.randint(1,100)) + ".avi")

    return is_video_processing, clip_tags, cap, cur_frame

if __name__ == '__main__':

    filepath = "../videos/"
    filename = "8min1.mp4"
    url = filepath + filename

    # open input video using videoCapture
    try:
        cap, frame_width, frame_height = fs.open_file(url)
    except IOError as error:
        print(error)
        print('Check the filename or camera.')


    vid_len = fs.get_video_length(url)
    print("vid len: " + str(vid_len))

    motionDetector = md.MotionDetect()
    completed_iterations = 0
    cur_frame = 0


    config = "../Yolo/yolov3.cfg"
    weights = "../Yolo/yolov3.weights"
    labels = "../Yolo/coco.names"
    conf = 0.85
    thresh = 0.8
    obj_det = od.Object_Detector(config, weights, labels, conf, thresh)

    clip_tags = set()

    is_video_processing = True
    while is_video_processing is True:
        is_video_processing, clip_tags, cap, cur_frame = process_segment(cap, motionDetector, cur_frame,
        vid_len, completed_iterations, obj_det, filename, clip_tags)
        completed_iterations += 1


    db.create_connection()
    db.save_clip(filename, vid_len, clip_tags, completed_iterations)