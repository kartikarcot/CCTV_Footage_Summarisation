import numpy as np
from random import uniform, random
import cv2
import skimage.measure
import copy


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

        frame_size = np.shape(tube_dict[0][0][0])[0] * np.shape(tube_dict[0][0][0])[1]

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
                        int_sum = np.sum(intersection)/255
                        shape = np.shape(intersection)
                        total = shape[0]*shape[1]*shape[2]*shape[3]
                        # print("shape: " + str(np.shape(intersection)))
                        normalized = int_sum/total
                        # print("normalized is "+str(normalized))
                        cost += np.sum(normalized)

        return cost * 10

    def length_cost(self, tube_dict, shift_dict):

        upper_limit = 0
        lower_limit = 0
        end_values = []
        start_values = []

        for key in tube_dict:
            start_values.append(tube_dict[key][1] + shift_dict[key])
            end_values.append(tube_dict[key][1] + tube_dict[key][2] + shift_dict[key])
            upper_limit += tube_dict[key][2]

            if tube_dict[key][2] > lower_limit:
                lower_limit = tube_dict[key][2]

        vid_end = max(end_values)
        vid_start = min(start_values)

        vid_len = vid_end - vid_start

        # print("UL: " + str(upper_limit))
        # print("LL: " + str(lower_limit))
        # print("Vid Len: " + str(vid_len))


        len_cost = (upper_limit - vid_len) / (upper_limit - lower_limit)

        if vid_len > upper_limit:
            return 10000
        else:
            return len_cost * 10

    def generate_config(self, tube_dict, Tmax, Tmin, T):

        shift_dict = {}

        for i, key in enumerate(list(tube_dict.keys())):
            ratio = (T-Tmin)/(Tmax-Tmin) - 0.01
            shift_dict[key] = int(uniform(-20, 20))

            # if tube_dict[key][1] + shift_dict[key] < 0:
            #     shift_dict[key] = -tube_dict[key][1]

#         print(shift_dict)
        return shift_dict



    def sigmoid(self, delta, T):
        return np.exp(-delta/T)

    def run(self, tube_dict_copy):

        tube_dict = copy.deepcopy(tube_dict_copy)
        for i, key1 in enumerate(list(tube_dict.keys())):
            print(np.shape(tube_dict_copy[key1][0]))
            print(np.shape(tube_dict[key1][0]))
            tube_dict[key1][0] = skimage.measure.block_reduce(np.asarray(tube_dict_copy[key1][0]), (1,4,4,1), np.max)
            print("shape of resized: " + str(np.shape(tube_dict[key1][0])))

        print("start times")
        for key in tube_dict:
            print(tube_dict[key][1])


        T = self.Tmax
        curr_config = self.generate_config(tube_dict, self.Tmax, self.Tmin, T)
        curr_cost = self.collision_cost(tube_dict, curr_config) + self.length_cost(tube_dict, curr_config)

        for epoch in range(0, self.num_epochs):
            print("epoch " + str(epoch))
            for it in range (0, self.num_iter):
                # print("iteration " + str(it))
                new_config = self.generate_config(tube_dict, self.Tmax, self.Tmin, T)

                # print("new config")
                # print(new_config)
                print("collision cost " + str(self.collision_cost(tube_dict, new_config)))
                print("length cost " + str(self.length_cost(tube_dict, new_config)))
                c_cost = self.collision_cost(tube_dict, new_config)
                l_cost = self.length_cost(tube_dict, new_config)
                new_cost = c_cost + l_cost

                delta = new_cost - curr_cost
                # print ("\ndelta is " + str(delta))
                # print ("\new cost is " + str(delta))
                # print ("\nold cost is " + str(delta))

                # exploitation
                if delta < 0:
                    print("updating... exploit")
                    print(str(c_cost) + " " + str(l_cost) + " " + str(new_cost))

#                     print(new_cost)
                    curr_cost = new_cost
                    curr_config = new_config

                    # Update the start times using shifts of new config
                    for key in tube_dict:
                        tube_dict[key][1] += new_config[key]
                    for key in tube_dict:
                        print(tube_dict[key][1:])
                else:
                    # exploration
                    print("sigmoid: "+ str(self.sigmoid(delta, T)))
                    if (random() < self.sigmoid(delta, T)):
                        print("updating - explore")
                        print(str(c_cost) + " " + str(l_cost) + " " + str(new_cost))
                        curr_cost = new_cost
                        curr_config = new_config

                        for key in tube_dict:
                            tube_dict[key][1] += new_config[key]
                        for key in tube_dict:
                            print(tube_dict[key][1:])

            T -= self.grad_T

        # push all negatives to positive time
        values = []
        for i, key1 in enumerate(list(tube_dict.keys())):
            values.append(tube_dict[key1][1])

        min_val = min(values)
        print(values)
        print("min val: " + str(min_val))
        if min_val < 0:
            for i, key1 in enumerate(list(tube_dict.keys())):
                tube_dict[key1][1] -= min_val

        # copy start times
        for i, key1 in enumerate(list(tube_dict.keys())):
            tube_dict_copy[key1][1] = tube_dict[key1][1]

        return tube_dict_copy