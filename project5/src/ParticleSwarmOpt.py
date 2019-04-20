import sys
import os
import matplotlib.pyplot as plt
import random
import math
import statistics as stat

class Swarm:

# --------------------------------- Initialization ----------------------------------------------- #
    def __init__(self, num_particles, inertia, cognition, social, w_width, w_height, max_velo, error_threshold, mode):
        self.num_particles = num_particles
        self.inertia = inertia
        self.cognition = cognition
        self.social = social
        self.w_width = w_width
        self.w_height = w_height
        self.max_velo = max_velo
        self.error_threshold = error_threshold
        self.mode = mode
        self.position = []
        self.personal_best = []
        self.personal_best_num = []
        self.x_velo = []
        self.y_velo = []
        self.global_best = (0, 0)
        self.global_best_num = -1000000
        self.ep_num = 0 #was jus ep_num
        # ----- Get random positioning ----- #
        for i in range(self.num_particles):
            x_pos = round(random.uniform(-50, 50), 2)
            y_pos = round(random.uniform(-50, 50), 2)
            self.position.append((x_pos, y_pos))
        # ----- Initialize velocities to 0, initialize personal bests to initial positions #
        for i in range(self.num_particles):
            self.x_velo.append(0)
            self.y_velo.append(0)
        self.personal_best = self.position.copy()
        self.personal_best_num = [-100000 for i in range(num_particles)] #chnge
        for i in range(num_particles): #chnge
            self.p_best(i, self.position[i])
        # ----- Global Best Initialization to best particle ----- #
        for i in self.position:
            self.g_best(i)

#----------------------------------------------End Init Phase-----------------------------------------#
    #calc global calcs
    def g_best(self, i):
        mdist = math.sqrt(math.pow(self.w_width, 2) + math.pow(self.w_height, 2)) / 2
        pdist = math.sqrt(math.pow((i[0] - 20), 2) + math.pow((i[1] - 7), 2))
        ndist = math.sqrt(math.pow((i[0] + 20), 2) + math.pow((i[1] + 7), 2))
        if self.mode == "DI-P1":
            Q = 100 * (1 - (pdist / mdist))
        else:
            Q = 9*max(0, (10-pow(pdist, 2)))+ 10*(1-(pdist/mdist)) + 70*(1-(ndist/mdist))
        if (Q > self.global_best_num):
            self.global_best_num = Q
            self.global_best = i

    #personal best calcs
    def p_best(self, i, j):
        mdist = math.sqrt(math.pow(self.w_width, 2) + math.pow(self.w_height, 2)) / 2
        pdist = math.sqrt(math.pow((j[0] - 20), 2) + math.pow((j[1] - 7), 2))
        ndist = math.sqrt(math.pow((j[0] + 20), 2) + math.pow((j[1] + 7), 2))
        if self.mode == "DI-P1":
            Q = 100 * (1 - (pdist / mdist))
        else:
            Q = 9*max(0, (10-pow(pdist, 2)))+ 10*(1-(pdist/mdist)) + 70*(1-(ndist/mdist))

        if (Q > self.personal_best_num[i]):
            self.personal_best_num[i] = Q
            self.personal_best[i] = j

    #tuple difference calc x direction
    def x_diff(self, i, j):
        return int(i[0]-j[0])
    #Tuple difference calc y direction
    def y_diff(self, i, j):
        return int(i[1]-j[1])

    def update_position(self, pos, x_velo, y_velo):
       x = int(pos[0])
       y = int(pos[1])
       #print(x, " ", y)
       x = x + x_velo
       y = y + y_velo
       if x > (self.w_width/2):
           x -= self.w_width
       if y > (self.w_height/2):
           y -= self.w_height
       if y < -self.w_height/2:
           y += self.w_height
       if x < -self.w_width/2:
           x += self.w_width
       pos = (x, y)
       return pos

    def get_global_dist(self):
        count = 0
        for i in self.position:
            c = math.sqrt( pow(i[0] - 20, 2) + pow(i[1] - 7, 2))
            if c < 0.001:
                count+=1
        return (1 - ((1.0*count)/(1.0*self.num_particles)))

#APRIL 15TH: WORKING, BEGIN REPORT AND THEN TEST OTHER CASES -- REMEMBER TO CHANGE SAVE NAMES!!
    def Update(self, run_num):
        error_data = []
        x_err = 10
        y_err = 10
        num_iter = 0
        while (x_err > self.error_threshold or y_err > self.error_threshold) and num_iter < 15000:
            num_iter += 1
            x_err = 0
            y_err = 0
            # portion below is for making scatter plots at specified epochs
            global temp
            if num_iter == 1 or num_iter == 10 or num_iter == 40 or num_iter == 100:
                temp = num_iter + run_num
                self.MakeScatter(temp)
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
            error_data.append((x_err, y_err))
            if self.mode == "DI-P1" or self.mode == "DI-P2":
                self.inertia -= .001
        self.ep_num = num_iter
        self.send_epochs()
        self.Plot_Err_vs_Epoch(error_data, num_iter, (run_num+1))

    #KEEP THIS FOR PROBLEM 2
    def MakeScatter(self, run_num):
        x = [i[0] for i in self.position]
        y = [i[1] for i in self.position]
        #do x y in global
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.scatter(self.global_best[0], self.global_best[1], s=30, c='b', marker="s", label='Global')
        if self.mode == "P2" or self.mode == "DI-P2":
            ax1.scatter(-self.global_best[0], -self.global_best[1], s=30, c='b', marker="s")
        ax1.scatter(x, y, s=10, c='r', marker="o", label='Particles')

        ax1.set_xlim(left=(-self.w_width / 2), right=(self.w_width / 2))
        ax1.set_ylim(bottom=(-self.w_height / 2), top=(self.w_height / 2))
        #ax1.set_xlim(left=(-self.w_width/2)+20, right=(self.w_width/2)-20)
        #ax1.set_ylim(bottom=(-self.w_height/2)+20, top=(self.w_height/2)-20)

        plt.axhline(0, color='black')
        plt.axvline(0, color='black')
        if self.mode != "DI-P1" and self.mode != "DI-P2":
            plt.title("Particles: " + str(self.num_particles)+", Inertia: " + str(self.inertia)+ ", Width:" + str(self.w_width)\
                    + ", Height: " + str(self.w_height))
        else:
            plt.title("Particles: " + str(self.num_particles) + ", Inertia: " + str(self.inertia))
        plt.legend(loc='upper right')
        path = "C:/Users/Sam/Documents/cs420/Project5/" + self.mode + "Charts"
        file_name = "/Scatter" + str(run_num)
        try:
            os.mkdir(path)
            print("Making dir...")
        except OSError:
            #print("Directory exists....Appending file...")
            pass
        fig.savefig(path + file_name)
        plt.close()
        #plt.show()

#Use epochs in bar chart to show when data reached
    def Plot_Err_vs_Epoch(self, error_data, epochs, run_num):
        x_err = [i[0] for i in error_data]
        y_err = [i[1] for i in error_data]

        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.plot(x_err, 'b', ls="solid", label="X Error")
        ax1.plot(y_err, 'r', ls="solid", label="Y Error")
        ax1.set_xlim(left=0, right=60)
        ax1.set_ylim(bottom=0, top=30)
        plt.xlabel("Epochs")
        plt.ylabel("Error")
        if self.mode != "DI-P1" and self.mode != "DI-P2":
            plt.title("Particles: " + str(self.num_particles)+", Inertia: " + str(self.inertia)+ ", Width:" + str(self.w_width)\
                    + ", Height: " + str(self.w_height))
        else:
            plt.title("Particles: " + str(self.num_particles) + ", Final Inertia: " + str(self.inertia))
        plt.legend(loc='upper right')
        path = "C:/Users/Sam/Documents/cs420/Project5/" +self.mode + "Charts"
        file_name = "/ExSet1Run" + str(run_num)
        try:
            os.mkdir(path)
        except OSError:
            #print("Directory exists....Appending file...")
            pass
        fig.savefig(path + file_name)
        plt.close()
        #plt.show()

    def send_epochs(self):
        return self.ep_num

#Number of epochs until convergence -- usefule for P1
def Epochs_to_Convergence(s, eps, runs):
    z = []
    ra = lambda: random.randint(0, 255)
    for x in range(10):
        z.append('#%02X%02X%02X' % (ra(), ra(), ra()))
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.bar(runs, eps, color=z)
    plt.xlabel("Runs")
    plt.ylabel("Number of Epochs")
    plt.xticks(runs)
    if s.mode != "DI-P1" and s.mode != "DI-P2":
        plt.title("Particles: " + str(s.num_particles) + ", Inertia: " + str(s.inertia) + ", Width:" + str(s.w_width) \
                  + ", Height: " + str(s.w_height))
    else:
        plt.title("Epochs to Convergence")
    path = "C:/Users/Sam/Documents/cs420/Project5/" + s.mode + "Charts"
    file_name = "/ExBarSet1Run"
    try:
        os.mkdir(path)
    except OSError:
        # print("Directory exists....Appending file...")
        pass
    fig.savefig(path + file_name)
    #plt.show()
    plt.close()

#Chart the percentage of particles that converged -- use this for P2
def chart_converged(s, pc, r):
    z = []
    ra = lambda: random.randint(0, 255)
    for x in range(10):
        z.append('#%02X%02X%02X' % (ra(), ra(), ra()))
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.bar(r, pc, color=z)
    plt.xlabel("Experiments")
    plt.ylabel("Percent Converged")
    plt.title("Particles: " + str(s.num_particles) + ", Inertia: " + str(s.inertia) + ", W:" + str(s.w_width) \
              + ", H: " + str(s.w_height))
    path = "C:/Users/Sam/Documents/cs420/Project5/" + s.mode + "Charts"
    file_name = "/BaseConRun"# + str(r)
    try:
        os.mkdir(path)
    except OSError:
        pass
    fig.savefig(path + file_name)
   # plt.show()
    plt.close()

def main():
    num_particles = int(sys.argv[1])
    inertia = float(sys.argv[2])
    cognition = float(sys.argv[3])
    social = float(sys.argv[4])
    w_width = int(sys.argv[5])
    w_height = int(sys.argv[6])
    max_velo = int(sys.argv[7])
    error_threshold = float(sys.argv[8])
    runs = int(sys.argv[9])
    mode = sys.argv[10]
    if mode == "P1" or mode == "P2" or mode == "DI-P1" or mode == "DI-P2":
        pass
    else:
        raise ValueError(mode)
    epoch_data = []
    r = []
    percent_converged = []
    for i in range(runs):
        swarm = Swarm(num_particles, inertia, cognition, social, w_width, w_height, max_velo, error_threshold, mode)
        swarm.Update(i)
        print("Experiment", (i+1), "Complete." )
        epoch_data.append(swarm.send_epochs())
        r.append(i+1)
        #swarm.MakeScatter((i+1)) For final swarms
        percent_converged.append(swarm.get_global_dist())
    print(epoch_data)
    print(stat.mean(epoch_data))
    chart_converged(swarm, percent_converged, r)
    Epochs_to_Convergence(swarm, epoch_data, r)


if __name__ == '__main__':
    main()