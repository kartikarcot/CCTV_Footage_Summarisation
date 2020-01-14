# simulated annealing optimizer tester

import optimize as op
import database as db
import numpy as np
from timeit import default_timer as timer

def test(filename="8min1.mp4", tags=['motorbike'], start_frame=0, end_frame=100000, min_length=30):

    # filepath = "../videos/"

    # url = filepath + filename

    db.create_connection()
    selected_tubes = db.get_tubes_by_query(filename, start_frame, end_frame, tags, min_length)
    phase1_iterations = db.get_clip_iterations(filename)

    print("Selected tube count: " + str(len(selected_tubes)))

    if len(selected_tubes) is 0:
        print("No tubes found for given query!")
        return

    tube_dict = {}

    total_tube_len = 0
    for i,tube in enumerate(selected_tubes):
        total_tube_len += tube.length

    prev_len = 0
    for i,tube in enumerate(selected_tubes):
        # volume, start time (initialize it to 0), length, actual start time
        tube_dict[i] = [np.asarray(tube.object_tube), 0, tube.length, tube.start]

    anneal = op.SimulatedAnnealing(30, 1, 70, 5)

    start = timer()

    for i in range(1, 11):
        # for j in range (0, 1):
        tube_dict = anneal.run(tube_dict, total_tube_len, 0.4)
    # for i,key in enumerate(tube_dict):
    #     print(tube_dict[key][1:])

    end = timer()
    print("Time: " + str(end - start))

if __name__ == "__main__":
    test()