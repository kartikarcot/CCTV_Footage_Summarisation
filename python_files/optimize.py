import numpy as np
from random import uniform, random
import cv2

class SimulatedAnnealing(object):
    def __init__(self, Tmax, Tmin, num_epochs, num_iter):
        self.Tmax = Tmax
        self.Tmin = Tmin
        self.num_epochs = num_epochs
        self.num_iter = num_iter
        self.grad_T = (self.Tmax - self.Tmin)/self.num_epochs
        self._blah = 10

    def collision_cost(self, tube_dict, shift_dict):
        '''
        Args:
            tube_dict = { id : [volume, start_time, length]}
            shift_dict = {id: shift}
        '''
        cost = 0

        for i, key1 in enumerate(list(tube_dict.keys())):
            for j, key2 in enumerate(list(tube_dict.keys())):
                #get initial times
                initial1 = tube_dict[key1][1]
                initial2 = tube_dict[key2][1]
                #chooose pairs of tubes
                if i < j:

                    #find intersection
                    start = max((tube_dict[key1][1] + shift_dict[key1]), (tube_dict[key2][1] + shift_dict[key2]))
                    end = min((tube_dict[key1][1] + shift_dict[key1] + tube_dict[key1][2]), (tube_dict[key2][1] + shift_dict[key2] + tube_dict[key2][2]))
                    #if intersection is present
                    if(end > start):
                        #identify parts of tubes wrt 0 which will participate in intersection
                        shift1 = tube_dict[key1][0][start - shift_dict[key1] - initial1 : end - shift_dict[key1] - initial1]
                        shift2 = tube_dict[key2][0][start - shift_dict[key2] -initial2 : end - shift_dict[key2] - initial2]

                        intersection = shift1*shift2
                        cost += np.sum(intersection)

        return cost

    def length_cost(self, tube_dict, shift_dict):

        values = []

        for key in tube_dict:
            values.append(tube_dict[key][1] + tube_dict[key][2] + shift_dict[key])

        return max(values)

    def generate_config(self, tube_dict, T):

        shift_dict = {}

        for i, key in enumerate(list(tube_dict.keys())):
            shift_dict[key] = int(uniform(-25, 50.0))
            if tube_dict[key][1] + shift_dict[key] < 0:
                shift_dict[key] = -tube_dict[key][1]

#         print(shift_dict)
        return shift_dict



    def sigmoid(self, delta, T):
        return 1/( 1 + np.exp(delta/T))

    def run(self, tube_dict):

        print("start times")
        for key in tube_dict:
                print(tube_dict[key][1])


        T = self.Tmax
        curr_config = self.generate_config(tube_dict, T)
        curr_cost = self.collision_cost(tube_dict, curr_config) + self.length_cost(tube_dict, curr_config)

        for epoch in range(0, self.num_epochs):
            for it in range (0, self.num_iter):
                new_config = self.generate_config(tube_dict, T)

#                 print("new config")
#                 print(new_config)
#                 print("collision cost " + str(self.collision_cost(tube_dict, new_config)))
#                 print("length cost " + str(self.length_cost(tube_dict, new_config)))
                new_cost = self.collision_cost(tube_dict, new_config) + self.length_cost(tube_dict, new_config)

#                 print(new_cost)

                delta = new_cost - curr_cost
#                 print ( "delta is " + str(delta))
                if (random() < self.sigmoid(delta, T)):
                    curr_config = new_config
                if delta < 0:
                    print("updating")

#                     print(new_cost)
                    curr_cost = new_cost

                    # Update the start times using shifts of new config
                    for key in tube_dict:
                        tube_dict[key][1] += new_config[key]
                    for key in tube_dict:
                        print(tube_dict[key][1:])

            T -= self.grad_T

        return tube_dict