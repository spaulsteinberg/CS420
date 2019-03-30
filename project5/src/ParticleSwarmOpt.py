import sys
import numpy as np
import matplotlib.pyplot as plt
import random
import math

class Swarm:
    x_coords = []
    y_coords = []
    position = []
    personal_best = []
    personal_best_num = []
    x_velo = []
    y_velo = []
    global_best = (0, 0)
    global_best_num = -1000000

# --------------------------------- Initialization ----------------------------------------------- #

    def __init__(self, num_particles, inertia, cognition, social, w_width, w_height, max_velo, error_threshold):
        self.num_particles = num_particles
        self.inertia = inertia
        self.cognition = cognition
        self.social = social
        self.w_width = w_width
        self.w_height = w_height
        self.max_velo = max_velo
        self.error_threshold = error_threshold
        # ----- Get random positioning ----- #

        for i in range(self.num_particles):
            x_pos = random.randint(-50, 50)
            y_pos = random.randint(-50, 50)
            self.x_coords.append(x_pos)
            self.y_coords.append(y_pos)
            self.position.append((x_pos, y_pos))

        # ----- Initialize velocities to 0, initialize personal bests to initial positions #

        for i in range(self.num_particles):
            self.x_velo.append(0)
            self.y_velo.append(0)
        self.personal_best = self.position.copy()
        self.personal_best_num = [-100000 for i in range(num_particles)]
        for i in range(num_particles):
            self.p_best(i, self.position[i])
            #print(self.personal_best, " ", self.personal_best_num[i])

        # ----- Global Best Initialization to best particle ----- #

        for i in self.position:
            self.g_best(i)
        #print('')
        #print(self.global_best, " ", self.global_best_num)

#----------------------------------------------End Init-----------------------------------------#

    def g_best(self, i):
        mdist = math.sqrt(math.pow(self.w_width, 2) + math.pow(self.w_height, 2)) / 2
        pdist = math.sqrt(math.pow((i[0] - 20), 2) + math.pow((i[1] - 7), 2))
        ndist = math.sqrt(math.pow((i[0] + 20), 2) + math.pow((i[1] + 7), 2))
        Q = 100 * (1 - (pdist / mdist))
        if (Q > self.global_best_num):
            self.global_best_num = Q
            self.global_best = i

    def p_best(self, i, j):
        mdist = math.sqrt(math.pow(self.w_width, 2) + math.pow(self.w_height, 2)) / 2
        pdist = math.sqrt(math.pow((j[0] - 20), 2) + math.pow((j[1] - 7), 2))
        ndist = math.sqrt(math.pow((j[0] + 20), 2) + math.pow((j[1] + 7), 2))
        Q = 100 * (1 - (pdist / mdist))
        if (Q > self.personal_best_num[i]):
            self.personal_best_num[i] = Q
            self.personal_best = j

    #def run(self):
        #err_t = 0
        #num_iter = 0
        #while err_t < self.error_threshold and num_iter < 15000:
            #num_iter += 1
            #for i in range(self.num_particles):




def main():
    num_particles = int(sys.argv[1])
    inertia = float(sys.argv[2])
    cognition = int(sys.argv[3])
    social = int(sys.argv[4])
    w_width = int(sys.argv[5])
    w_height = int(sys.argv[6])
    max_velo = int(sys.argv[7])
    error_threshold = float(sys.argv[8])
    swarm = Swarm(num_particles, inertia, cognition, social, w_width, w_height, max_velo, error_threshold)

if __name__ == '__main__':
    main()