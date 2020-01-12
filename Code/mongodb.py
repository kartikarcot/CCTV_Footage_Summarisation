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
connect('test')


################
class Tube(Document):
    desc = StringField(max_length=50)
    time_start = DateTimeField()
    time_end = DateTimeField()
    tags = ListField(StringField(max_length=50))

tube = Tube(desc='Using MongoEngine')
tube.time_start = datetime.datetime.now()
tube.time_end = datetime.datetime.now() + datetime.timedelta(seconds=60)
tube.tags = ['person', 'car']
tube.save()

for tube in Tube.objects():
    print(tube.desc)
########################
