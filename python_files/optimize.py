import numpy as np
import random
import cv2
import skimage.measure
import copy

import pandas as pd


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
                    start = max((shift_dict[key1]), (shift_dict[key2]))
                    end = min((shift_dict[key1] + tube_dict[key1][2]), (shift_dict[key2] + tube_dict[key2][2]))
                    #if intersection is present
                    if(end > start):
                        #identify parts of tubes wrt 0 which will participate in intersection
                        shift1 = tube_dict[key1][0][start - shift_dict[key1] : end - shift_dict[key1]]
                        shift2 = tube_dict[key2][0][start - shift_dict[key2] : end - shift_dict[key2]]

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
        total_tube_len = 0

        for key in tube_dict:
            start_values.append(shift_dict[key])
            end_values.append(tube_dict[key][2] + shift_dict[key]) # length + start val
            upper_limit += tube_dict[key][2]    # lengths

            if tube_dict[key][2] > lower_limit:
                lower_limit = tube_dict[key][2]

        vid_end = max(end_values)
        vid_start = min(start_values)

        vid_len = vid_end - vid_start

        # print("UL: " + str(upper_limit))
        # print("LL: " + str(lower_limit))
        # print("Vid Len: " + str(vid_len))


        len_cost = (vid_len - lower_limit) / (upper_limit - lower_limit)

        if vid_len > upper_limit:
            return 10000
        else:
            return len_cost

    def generate_config(self, tube_dict, Tmax, Tmin, T, max_length):

        shift_dict = {}

        for i, key in enumerate(list(tube_dict.keys())):

            shift_dict[key] = int(random.uniform(0, 1) * max_length * 0.5)

            # if tube_dict[key][1] + shift_dict[key] < 0:
            #     shift_dict[key] = -tube_dict[key][1]

#         print(shift_dict)
        return shift_dict



    def sigmoid(self, delta, T):
        return np.exp(-delta/T)

    def run(self, tube_dict_copy, max_length):

        tube_dict = copy.deepcopy(tube_dict_copy)
        for i, key1 in enumerate(list(tube_dict.keys())):
            print(np.shape(tube_dict_copy[key1][0]))
            print(np.shape(tube_dict[key1][0]))
            tube_dict[key1][0] = skimage.measure.block_reduce(np.asarray(tube_dict_copy[key1][0]), (1,4,4,1), np.max)
            print("shape of resized: " + str(np.shape(tube_dict[key1][0])))

        print("start times")
        for key in tube_dict:
            print(tube_dict[key][1])

        final_dict = {'Epoch no': [], 'Collision cost': [], 'Length cost': [], 'Total cost': [],
            #'Energy': [], 'Temp': [], 'Random': [], 'Sigmoid': []
        }

        T = self.Tmax
        curr_config = self.generate_config(tube_dict, self.Tmax, self.Tmin, T, max_length)
        curr_cost = (self.collision_cost(tube_dict, curr_config) * 0.8 + self.length_cost(tube_dict, curr_config) * 0.2) * 1000

        for epoch in range(0, self.num_epochs):
            print("epoch " + str(epoch))
            for it in range (0, self.num_iter):
                # print("iteration " + str(it))
                new_config = self.generate_config(tube_dict, self.Tmax, self.Tmin, T, max_length)

                # print("new config")
                # print(new_config)
                print("collision cost " + str(self.collision_cost(tube_dict, new_config)))
                print("length cost " + str(self.length_cost(tube_dict, new_config)))
                c_cost = self.collision_cost(tube_dict, new_config)
                l_cost = self.length_cost(tube_dict, new_config)
                new_cost = (c_cost * 0.8 + l_cost * 0.2) * 1000

                delta = new_cost - curr_cost
                # print ("\ndelta is " + str(delta))
                # print ("\new cost is " + str(delta))
                # print ("\nold cost is " + str(delta))

                # exploitation
                if delta < 0:
                    print("updating... exploit")
                    print(str(c_cost) + " " + str(l_cost) + " " + str(new_cost))

                    final_dict['Epoch no'].append(epoch)
                    final_dict['Collision cost'].append(c_cost)
                    final_dict['Length cost'].append(l_cost)
                    final_dict['Total cost'].append(new_cost/1000)

#                     print(new_cost)
                    curr_cost = new_cost
                    curr_config = new_config

                    # Update the start times using shifts of new config
                    for key in tube_dict:
                        tube_dict[key][1] = new_config[key]
                    for key in tube_dict:
                        print(tube_dict[key][1:])
                else:
                    # exploration
                    sigmoid_val = self.sigmoid(delta, T)
                    print("sigmoid: "+ str(sigmoid_val))
                    random_val = random.random()

                    if (random_val < sigmoid_val):
                        print("updating - explore")
                        print(str(c_cost) + " " + str(l_cost) + " " + str(new_cost))
                        curr_cost = new_cost
                        curr_config = new_config


                        # final_dict['Energy'].append(delta)
                        # final_dict['Temp'].append(T)
                        # final_dict['Random'].append(random_val)
                        # final_dict['Sigmoid'].append(sigmoid_val)
                        final_dict['Epoch no'].append(epoch)
                        final_dict['Collision cost'].append(c_cost)
                        final_dict['Length cost'].append(l_cost)
                        final_dict['Total cost'].append(new_cost/1000)

                        for key in tube_dict:
                            tube_dict[key][1] = new_config[key]
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

        for i, key1 in enumerate(list(tube_dict.keys())):
            tube_dict[key1][1] -= min_val

        # copy start times
        for i, key1 in enumerate(list(tube_dict.keys())):
            tube_dict_copy[key1][1] = tube_dict[key1][1]

        df = pd.DataFrame(final_dict, index=None)
        df.to_excel('Cost' + str(random.randint(1,1000)) + '.xlsx')

        return tube_dict_copy