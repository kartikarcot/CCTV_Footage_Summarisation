import numpy as np
import random
import cv2
import skimage.measure
import copy

import pandas as pd
import json

COLLISION_COST_WEIGHT = 0.6
LENGTH_COST_WEIGHT = 0.4

class SimulatedAnnealing(object):
    def __init__(self, Tmax, Tmin, num_epochs, num_iter):
        self.Tmax = Tmax
        self.Tmin = Tmin
        self.num_epochs = num_epochs
        self.num_iter = num_iter
        self.grad_T = (self.Tmax - self.Tmin)/self.num_epochs

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
                # get initial times
                initial1 = tube_dict[key1][1]
                initial2 = tube_dict[key2][1]
                # choose pairs of tubes
                if i < j:

                    # find intersection
                    start = max((tube_dict[key1][1] + shift_dict[key1]), (tube_dict[key2][1] + shift_dict[key2]))
                    end = min((tube_dict[key1][1] + shift_dict[key1] + tube_dict[key1][2]), (tube_dict[key2][1] + shift_dict[key2] + tube_dict[key2][2]))
                    # if intersection is present
                    if(end > start):
                        # identify parts of tubes wrt 0 which will participate in intersection
                        shift1 = tube_dict[key1][0][start - shift_dict[key1] - initial1 : end - shift_dict[key1] - initial1]
                        shift2 = tube_dict[key2][0][start - shift_dict[key2] - initial2 : end - shift_dict[key2] - initial2]

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
            start_values.append(tube_dict[key][1] + shift_dict[key])
            end_values.append(tube_dict[key][1] + tube_dict[key][2] + shift_dict[key]) # length + start val
            upper_limit += tube_dict[key][2]    # lengths

            if tube_dict[key][2] > lower_limit:
                lower_limit = tube_dict[key][2]

        vid_end = max(end_values)
        vid_start = min(start_values)

        vid_len = vid_end - vid_start

        # print("UL: " + str(upper_limit))
        # print("LL: " + str(lower_limit))
        # print("Vid Len: " + str(vid_len))

        if upper_limit > lower_limit:
            len_cost = (vid_len - lower_limit) / (upper_limit - lower_limit)
        else:
            len_cost = upper_limit

        len_cost = np.exp(5*(len_cost-1))

        if vid_len > upper_limit:
            return vid_len/upper_limit
        else:
            return len_cost

    def generate_config(self, tube_dict, Tmax, Tmin, T, max_length, config_variable):

        shift_dict = {}

        for i, key in enumerate(list(tube_dict.keys())):

            # ratio = (T-Tmin)/(Tmax-Tmin)
            ratio = 1
            shift_dict[key] = int(random.uniform(-1, 1) * (config_variable * max_length) * ratio)

#         print(shift_dict)
        return shift_dict

    def generate_initial_config(self, tube_dict, max_length):

            shift_dict = {}

            total_cost = 10000000

            tube_dict_copy = copy.deepcopy(tube_dict)

            for iters in range(0, 20):
                # generate a random config
                for i, key in enumerate(list(tube_dict.keys())):
                    # set the initial position in tube_dict itself
                    tube_dict[key][1] = int(random.uniform(0, 1) * max_length * 0.5)
                    # set shift to 0
                    shift_dict[key] = 0

                # calc cost
                c_cost = self.collision_cost(tube_dict, shift_dict)
                l_cost = self.length_cost(tube_dict, shift_dict)
                new_cost = (c_cost * COLLISION_COST_WEIGHT + l_cost * LENGTH_COST_WEIGHT) * 1000

                if new_cost < total_cost:
                    # update values
                    for i, key in enumerate(list(tube_dict.keys())):
                        tube_dict_copy[key][1] = tube_dict[key][1]

    #         print(shift_dict)
            return tube_dict_copy



    def sigmoid(self, delta, T):
        return np.exp(-delta/T)

    def run(self, tube_dict_copy, max_length, config_variable):

        tube_dict = copy.deepcopy(tube_dict_copy)

        for i, key1 in enumerate(list(tube_dict.keys())):
            # print(np.shape(tube_dict_copy[key1][0]))
            # print(np.shape(tube_dict[key1][0]))
            tube_dict[key1][0] = skimage.measure.block_reduce(np.asarray(tube_dict_copy[key1][0]), (1,4,4,1), np.max)
            # print("shape of resized: " + str(np.shape(tube_dict[key1][0])))

        tube_dict = self.generate_initial_config(tube_dict, max_length)

        print("start times")
        for key in tube_dict:
            pass# print(tube_dict[key][1])

        # setup visualisation dict
        ################################
        visualise_dict = {
            'clip_length': max_length,
            'tubeLen': [],
            'init': [],
            'iter': []
        }

        for i, key in enumerate(list(tube_dict.keys())):
            start = tube_dict[key][1]
            length = tube_dict[key][2]
            visualise_dict['init'].append(start)
            visualise_dict['tubeLen'].append(length)
        #############################################


        final_dict = {'Epoch no': [], 'Collision cost': [], 'Length cost': [], 'Total cost': [],
            #'Energy': [], 'Temp': [], 'Random': [], 'Sigmoid': []
        }

        T = self.Tmax
        curr_config = self.generate_config(tube_dict, self.Tmax, self.Tmin, T, max_length, config_variable)
        curr_cost = (self.collision_cost(tube_dict, curr_config) * COLLISION_COST_WEIGHT +
            self.length_cost(tube_dict, curr_config) * LENGTH_COST_WEIGHT) * 1000

        for epoch in range(0, self.num_epochs):
            # print("epoch " + str(epoch))
            for it in range (0, self.num_iter):
                # print("iteration " + str(it))
                new_config = self.generate_config(tube_dict, self.Tmax, self.Tmin, T, max_length, config_variable)

                # print("new config")
                # print(new_config)
                # print("collision cost " + str(self.collision_cost(tube_dict, new_config)))
                # print("length cost " + str(self.length_cost(tube_dict, new_config)))
                c_cost = self.collision_cost(tube_dict, new_config)
                l_cost = self.length_cost(tube_dict, new_config)
                new_cost = (c_cost * COLLISION_COST_WEIGHT + l_cost * LENGTH_COST_WEIGHT) * 1000

                delta = new_cost - curr_cost
                # print ("\ndelta is " + str(delta))
                # print ("\new cost is " + str(delta))
                # print ("\nold cost is " + str(delta))

                # exploitation
                if delta < 0:
                    # print("updating... exploit")
                    # print(str(c_cost) + " " + str(l_cost) + " " + str(new_cost))

                    final_dict['Epoch no'].append(epoch)
                    final_dict['Collision cost'].append(c_cost)
                    final_dict['Length cost'].append(l_cost)
                    final_dict['Total cost'].append(new_cost/1000)

#                     print(new_cost)
                    curr_cost = new_cost
                    curr_config = new_config

                    # Update the start times using shifts of new config
                    for key in tube_dict:
                        tube_dict[key][1] += new_config[key]
                        # print(tube_dict[key][1:])

                    # visualsation data
                    #################################
                    iter_dict = {
                        'epoch': epoch,
                        'iteration': (epoch * self.num_iter) + it,
                        'start': [],
                        'collisionCost': c_cost,
                        'lengthCost': l_cost,
                        'totalCost': new_cost/1000
                    }

                    # normalize to 0 and append start vals
                    vals = []
                    for key in tube_dict:
                        vals.append(tube_dict[key][1])
                        # iter_dict['start'].append(tube_dict[key][1])

                    min_val = min(vals)

                    for key in tube_dict:
                        iter_dict['start'].append(tube_dict[key][1] - min_val)

                    visualise_dict['iter'].append(iter_dict)
                    #################################

                # else:
                #     # exploration
                #     sigmoid_val = self.sigmoid(delta, T)
                #     # print("sigmoid: "+ str(sigmoid_val))
                #     random_val = random.random()

                #     if (random_val < sigmoid_val):
                #         # print("updating - explore")
                #         # print(str(c_cost) + " " + str(l_cost) + " " + str(new_cost))
                #         curr_cost = new_cost
                #         curr_config = new_config


                #         # final_dict['Energy'].append(delta)
                #         # final_dict['Temp'].append(T)
                #         # final_dict['Random'].append(random_val)
                #         # final_dict['Sigmoid'].append(sigmoid_val)
                #         final_dict['Epoch no'].append(epoch)
                #         final_dict['Collision cost'].append(c_cost)
                #         final_dict['Length cost'].append(l_cost)
                #         final_dict['Total cost'].append(new_cost/1000)

                #         for key in tube_dict:
                #             tube_dict[key][1] += new_config[key]
                #             # print(tube_dict[key][1:])

                #         # visualsation data
                #         #################################
                #         iter_dict = {
                #             'epoch': epoch,
                #             'iteration': (epoch * self.num_iter) + it,
                #             'start': [],
                #             'collisionCost': c_cost,
                #             'lengthCost': l_cost,
                #             'totalCost': new_cost/1000
                #         }

                #         # normalize to 0 and append start vals
                #         vals = []
                #         for key in tube_dict:
                #             vals.append(tube_dict[key][1])
                #             # iter_dict['start'].append(tube_dict[key][1])

                #         min_val = min(vals)

                #         for key in tube_dict:
                #             iter_dict['start'].append(tube_dict[key][1] - min_val)

                #         visualise_dict['iter'].append(iter_dict)
                #         #################################
            T -= self.grad_T

        # push all negatives to positive time
        values = []
        for i, key1 in enumerate(list(tube_dict.keys())):
            values.append(tube_dict[key1][1])

        min_val = min(values)
        # print(values)
        print("min val: " + str(min_val))

        for i, key1 in enumerate(list(tube_dict.keys())):
            tube_dict[key1][1] -= min_val

        # copy start times
        for i, key1 in enumerate(list(tube_dict.keys())):
            tube_dict_copy[key1][1] = tube_dict[key1][1]

        df = pd.DataFrame(final_dict, index=None)
        df.to_excel("Cost" + str(random.randint(1,10000)) + ".xlsx")

        with open("data_file_" + str(random.randint(1,10000)) + ".json", "w") as write_file:
            json.dump(visualise_dict, write_file)

        return tube_dict_copy