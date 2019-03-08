import sys
import csv
import random
import math
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
def zero_grid(grid, row, col):
    for i in range(0, row):
        y = 0
        grid.append([y])
        for j in range(0, col):
            x = 0
            grid[i].append(x)


# Generate a grid of cells, values between 1 and -1
def initialize_grid(grid, row, col):
    for i in range(0, row):
        y = random.randrange(0, 2)
        if y == 0:
            y = -1
        grid.append([y])
        for j in range(0, col):
            x = random.randrange(0, 2)
            if x == 0:
                x = -1
            grid[i].append(x)


def distance_between_two_cells(x1, x2, y1, y2):
    xdist = abs(x1 - y1)
    ydist = abs(x2 - y2)
    if xdist > 15:
        xdist = 30 - xdist
    if ydist > 15:
        ydist = 30 - ydist
    dist = xdist + ydist
    return dist


def generate_image(grid, row, col, id):
    filename = "Experiment" + str(id) + ".pgm"
    try:
        fout = open(filename, 'w+')
    except IOError:
        print('Error writing to: ' + filename)
        sys.exit()
    header = "P2" + '\n' + "30 30" + '\n' + str(255) + '\n'
    fout.write(header)
    for i in range(0, row):
        for j in range(0, col):
            if grid[i][j] == -1:
                y = "255 "
                fout.write(y)
            if grid[i][j] == 1:
                x = "0 "
                fout.write(x)
        fout.write('\n')
    fout.close()


def calc_correlation(grid):
    first = 0.0
    for l in range(15):
        second = 0.0
        if l == 0:
            second = 1
        else:
            for i in range(30):
                for j in range(30):
                    first+=grid[i][j]
                    first /= 900
                    first*=first
                    for i2 in range(30):
                        for j2 in range(30):
                            dist = distance_between_two_cells(i, j, i2, j2)
                            if l == dist:
                                second += (grid[i][j] * grid[i2][j2])
            second /= (3600*l)
        correlation_list.append(abs(second-first))


def calc_entropy(grid):
    con_sum = 0.0
    N = 30.0
    for i in range(0, 30):
        for j in range(0, 30):
            con_sum += ((1 + grid[i][j])/2)
    pos = (1.0/(N*N))*con_sum
    neg = 1.0 - pos
    if pos == 0 or neg == 0:
        if pos == 0:
            H = -1*neg*math.log2(neg)
        elif neg == 0:
            H = -1*pos*math.log2(pos)
    else:
        Hpos = (pos*math.log2(pos))
        Hneg = (neg*math.log2(neg))
        H = -1*(Hpos+Hneg)
    return H


def calc_joint_entropy(grid):
    for distance in range(15):
        inner_sum = 0
        inner_sum_neg = 0
        pos_neg = 0
        for i in range(30):
            for j in range(30):
                for i2 in range(30):
                    for col1 in range(30):
                        dist = distance_between_two_cells(i, j, i2, col1)
                        if dist == distance:
                            inner_sum += (((1+grid[i][j])/2) * ((1 + grid[i2][col1])/2))
                            inner_sum_neg += (((1-grid[i][j])/2) * ((1 - grid[i2][col1])/2))
        if distance == 0:
            inner_sum = inner_sum / 9000
            inner_sum_neg = inner_sum_neg / 9000
        else:
            inner_sum = (inner_sum / (3600*distance))
            inner_sum_neg = (inner_sum_neg / (3600 * distance))

        pos_neg = 1 - inner_sum - inner_sum_neg
        h1 = 0
        h2 = 0
        h3 = 0
        if inner_sum > 0:
            h1 = inner_sum*math.log2(inner_sum)
        if inner_sum_neg > 0:
            h2 = inner_sum_neg * math.log2(inner_sum_neg)
        if pos_neg > 0:
            h3 = pos_neg * math.log2(pos_neg)
        H = -1.0*(h1+h2+h3)
        joint_entropy.append(H)


def calc_mutual_info(H):
    for dist in range(0, 15):
        mutual_info.append(((2*H)-joint_entropy[dist]))

def update_grid(grid, gridSize, id):
    count = 20
    while count > 0:
        updated_grid = []
        total_cells = 900
        zero_grid(updated_grid, gridSize, gridSize)
        while total_cells > 0:
            while True:
                row = random.randrange(0, 30)
                col = random.randrange(0, 30)
                if updated_grid[row][col] == 0:
                    updated_grid[row][col] = 1
                    break
            total_cells = total_cells - 1
            near_cell = 0
            far_cell = 0
            for i in range(0, 30):
                for j in range(0, 30):
                    dist = distance_between_two_cells(row, col, i, j)
                    if dist < r1:
                        near_cell = near_cell + grid[i][j]
                    elif dist >= r1 and dist < r2:
                        far_cell = far_cell + grid[i][j]
            j1prod = j1 * near_cell
            j2prod = j2 * far_cell
            prod = j1prod + j2prod + h
            if prod >= 0:
                grid[row][col] = 1
            else:
                grid[row][col] = -1
            #print(total_cells)
        count = count - 1
    generate_image(grid, gridSize, gridSize, id)
    return grid


gridSize = 30
j1 = float(input("Enter j1: "))
j2 = float(input("Enter j2: "))
r1 = float(input("Enter r1: "))
r2 = float(input("Enter r2: "))
h = float(input("Enter h: "))
plt_answer = input("Plot results? : ")
correlation_list = []
joint_entropy = []
mutual_info = []


def main():
    user_args = input("Enter a unique ID number: ")
    id = int(user_args)
    grid = []
    initialize_grid(grid, gridSize, gridSize) # probably move this out of the for loop to initialize once
    grid = update_grid(grid, gridSize, id)
    calc_correlation(grid)
   # print(correlation_list)
    entropy = calc_entropy(grid)
    #print(entropy)
    calc_joint_entropy(grid)
    #print(joint_entropy)
    calc_mutual_info(entropy)
    #print(mutual_info)
    res_file = open("AICA.csv", 'a')
    wr = csv.writer(res_file, delimiter=",")
    for i in joint_entropy:
        wr.writerow([i, ])
    for i in mutual_info:
        wr.writerow([i, ])
    for i in correlation_list:
        wr.writerow([i, ])
    if plt_answer == "yes":
        distances = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        joint_entropy.pop(0)
        mutual_info.pop(0)
        correlation_list.pop(0)
        fontP = FontProperties()
        fontP.set_size('small')
        plt.plot(distances, joint_entropy, 'b-.', label="Joint Entropy")
        plt.plot(distances, mutual_info, color='orange', label="Mutual Info")
        plt.plot(distances, correlation_list, 'r-.', label="Correlation")
        plt.legend(prop=fontP)
        plt.title("j1: " + str(j1) + " j2: " + str(j2) + " r1: " + str(r1) + " r2: " + str(r2) + " h: " + str(h))
        plt.show()


if __name__ == '__main__':
    main()
