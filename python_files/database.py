# testing mongodb using mongoengine ODM


# Tubes Database Fields
# _id : id
# camera_id : int
# time_begin : date
# time_end : date
# duration : int
# frame_count : int
# frame_rate : int
# activity_size : int
# spatial_area : int
# phase_change : bool
# speed : int
# tube_id : uuid
# tags : list<string>

from mongoengine import *
import datetime
import uuid
import datetime

import numpy as np
import tube as tb

FILEPATH = "../storage/"

################
class TubeDB(Document):
    created_date = DateTimeField()
    clip_name = StringField(max_length=50)
    tube_id = StringField(max_length=100)
    start = IntField()
    end = IntField()
    length = IntField()
    tags = ListField(StringField(max_length=20))

class Clip(Document):
    created_date = DateTimeField()
    clip_name = StringField(max_length=50)
    length = IntField()
    iterations = IntField()
    tags = ListField(StringField(max_length=20))

# tube = TubeDB()
# tube.clip_name = "abc"
# tube.file_name = "bcd"
# tube.time_start = 3
# tube.time_end = 20
# tube.tags = ['person', 'car']
# tube.save()

# for tube in TubeDB.objects():
#     print(tube.clip_name)
########################

def create_connection():
    connect('summary', host='127.0.0.1:27017')

def save_tubes(tubes, clip_name):
    """
    args: takes a list of tube objects
    """

    for tube in tubes:

        tube_id = str(uuid.uuid1())

        tubedb = TubeDB()
        tubedb.created_date = datetime.datetime.now()
        tubedb.clip_name = clip_name
        tubedb.tube_id = tube_id
        tubedb.start = tube.start
        tubedb.end = tube.end
        tubedb.length = tube.length
        tubedb.tags = list(tube.tags)

        if len(list(tube.tags)) > 0:
            # save metadata in DB
            tubedb.save()

            # save the files to disk

            filename = FILEPATH + tube_id
            np.savez_compressed(filename, mask_tube=tube.mask_tube, object_tube=tube.object_tube)

def save_clip(clip_name, length, tags, iterations):
    # save the clip details
    clip = Clip()
    clip.created_date = datetime.datetime.now()
    clip.clip_name = clip_name
    clip.length = length
    clip.iterations = iterations
    clip.tags = list(tags)
    clip.save()



def get_clips():
    """
    Return the clips that are stored in DB
    """
    clips = []
    for clip in Clip.objects():
        clips.append(str(clip.clip_name))

    return clips

def get_num_clips():
    """
    Return number of clips that are stored in DB
    """
    return len(Clip.objects())

def get_clip_iterations(clip_name):
    """
    Return clip iterations given clip name
    """
    for clip in Clip.objects(clip_name=clip_name):
        # we expect only 1 clip of the given name
        return int(clip.iterations)

    return 0

def get_clip_length(clip_name):
    """
    Return clip iterations given clip name
    """
    for clip in Clip.objects(clip_name=clip_name):
        # we expect only 1 clip of the given name
        return int(clip.length)

    return 0

def get_tubes_by_query(clip_name, start, end, tags, min_length):
    """
    Return the tubeDB objects using query
    """

    tubes = []

    for tubedb in TubeDB.objects(clip_name=clip_name, start__gte=start, end__lte=end, length__gte=min_length):
        # print(str(tubedb.clip_name) + " " + str(tubedb.tags))

        tube = tb.Tube()
        tube.start = tubedb.start
        tube.end = tubedb.end
        tube.length = tubedb.length

        # select based on tags
        qset = set(tags)
        tset = set(tubedb.tags)

        if(bool(qset.intersection(tset))):

            filename = FILEPATH + str(tubedb.tube_id) + ".npz"
            loaded_file = np.load(filename)
            tube.mask_tube = loaded_file['mask_tube']
            tube.object_tube = loaded_file['object_tube']

            # print(np.shape(tube.mask_tube))
            # print(np.shape(tube.object_tube))

            tubes.append(tube)

    return tubes


