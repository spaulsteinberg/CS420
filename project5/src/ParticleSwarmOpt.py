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
            x_pos = round(random.uniform(-50, 50), 2)
            y_pos = round(random.uniform(-50, 50), 2)
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
            #print(self.personal_best[i], " ", self.personal_best_num[i])

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
            self.personal_best[i] = j

    def x_diff(self, i, j):
        dif = abs(i[0] - j[0])
        return dif

    def y_diff(self, i, j):
        dif = abs(i[1] - j[1])
        return dif

    def update_position(self, pos, x_velo, y_velo):
       x = int(pos[0])
       y = int(pos[1])
       x = x + x_velo
       y = y + y_velo
       pos = (x, y)
       return pos

    def run(self):
        x_err = 0
        y_err = 0
        num_iter = 0
        while (x_err < self.error_threshold or y_err < self.error_threshold) and num_iter < 15000:
            num_iter += 1
            for i in range(self.num_particles):
                r_1 = random.uniform(0.0, 1.0)
                r_2 = random.uniform(0.0, 1.0)
                self.x_velo[i] = self.inertia * self.x_velo[i] + self.cognition * r_1 * \
                                 self.x_diff(self.personal_best[i], self.position[i]) + self.social * r_2 * self.x_diff(self.global_best, self.position[i])
                self.y_velo[i] = self.inertia * self.y_velo[i] + self.cognition * r_1 * \
                                 self.y_diff(self.personal_best[i], self.position[i]) + self.social * r_2 * self.y_diff(self.global_best, self.position[i])
                if (math.pow(self.x_velo[i], 2) + math.pow(self.y_velo[i], 2)) > math.pow(self.max_velo, 2):
                    self.x_velo[i] = (self.max_velo / math.sqrt(math.pow(self.x_velo[i], 2) + math.pow(self.y_velo[i], 2))) * \
                                     self.x_velo[i]
                    self.y_velo[i] = (self.max_velo / math.sqrt(math.pow(self.x_velo[i], 2) + math.pow(self.y_velo[i], 2))) * \
                                     self.y_velo[i]
                self.position[i] = self.update_position(self.position[i], self.x_velo[i], self.y_velo[i])
                self.p_best(i, self.position[i])
                self.g_best(self.position[i])
                x_err = 0
                y_err = 0
                for k in range(self.num_particles):
                    x_err += math.pow(self.position[k][0] - self.global_best[0], 2)
                    y_err += math.pow(self.position[k][1] - self.global_best[1], 2)
            x_err = math.sqrt((1/(2*self.num_particles)) *x_err)
            y_err = math.sqrt((1 / (2 * self.num_particles)) * y_err)
            print(x_err)
            print(y_err)
                #print(self.personal_best[i], " ", self.global_best)

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
    swarm.run()
if __name__ == '__main__':
    main()