#Author: Gabriel Castillo Rosales

#Imports
import numpy as np
import matplotlib.pyplot as plt

#classes
class Particle:

    def __init__(self, p0, v0, box):
        self.pos, self.vel, = p0, v0                 # p0 is [x,y]
        self.box = box                               # v0 is float
        self.timer = 0
        self.taken = [p0]
        self.step_counter = 0

    def update(self, angle, dl, dt):
        #Calc
        angle = angle*(np.pi/180)
        temp_pos = [self.pos[0] + self.vel*np.cos(angle), self.pos[1] + self.vel*np.sin(angle)]

        #Check isWall and isExit
        isWall = self.box.isWall(temp_pos)
        isExit = self.box.isExit(temp_pos)

        if not isWall and not isExit:
            self.taken.append(self.pos)
            self.timer += dt
            self.pos = temp_pos
            self.step_counter += 1
            self.box.update_gap(dl)

        if isExit:
            self.timer += dt
            self.taken.append(self.pos)
            self.taken.append(temp_pos)
            self.pos = temp_pos
            self.step_counter += 1
            self.box.update_gap(dl)
            return [self.timer, self.taken]

        elif isWall:
            self.timer += dt
            self.step_counter += 1
            self.taken.append(self.pos)
            if temp_pos[0] >= self.box.X:
                temp_pos[0] = self.box.X
            if temp_pos[0] <= 0:
                temp_pos[0] = 0
            if temp_pos[1] >= self.box.Y:
                temp_pos[1] = self.box.Y
            if temp_pos[1] <= 0:
                temp_pos[1] = 0
            else:
                temp_pos = temp_pos
            self.taken.append(temp_pos)
            self.box.update_gap(dl)
            if self.box.isExit(temp_pos):
                return [self.timer, self.taken]
        
class Box:

    def __init__(self, dims, gap):
        self.X, self.Y = dims[0], dims[1]
        self.gap = gap
        self.left_gap, self.right_gap = 0.5*(self.X - self.gap), 0.5*(self.X + self.gap)

    def isWall(self, pos):
        x, y = pos[0], pos[1]

        if x == 0 or x == self.X:
            return True
        elif y == 0 or y == self.Y:
            return True
        else:
            return False

    def isExit(self, pos):
        x, y = pos[0], pos[1]

        if x >= self.left_gap or x <= self.right_gap:
            if y >= self.Y:
                return True
            else:
                return False
        else:
            return False

    def update_gap(self, dl):
        self.gap = self.gap - dl
        self.left_gap, self.right_gap = 0.5*(self.X - self.gap), 0.5*(self.X + self.gap)


#Functions
def plot(data, plot_name='', fname=''):
    
    dx, dy = data[0], data[1]
    plt.cla()
    for i in range(0, len(dx)-1):
        plt.arrow(dx[i], dy[i], dx[i+1], dy[i+1], color="black")
    plt.title(plot_name)
    plt.savefig(fname)

def sim(n, gap=0.5, v0=0.2, p0=[1,1]):
    gen = np.random.default_rng()
    seed = gen.random()

    box = Box((2,2), gap)
    
    dot = Particle(p0, v0, box)
    angle_arr = gen.uniform(low=0, high=360, size=100*n)
    
    dt = 0.01
    for i in range(0, len(angle_arr)):
        steps = dot.update(angle_arr[i], 1/n , dt)
        if steps != None:
            if len(steps) == 2 and type(steps[0]) != type(steps[1]):
                break
            else:
                continue
        else:
            continue
    return dot.taken

for i in range(0, 10):
    print("run: {}".format(str(i)))
    for r in range(0, 5000):
        fname = '/sim_n{}.csv'.format(str(r))
        run = sim(60, p0=[0.5, (i*2)/10])
        with open('Data/Sim/{}/{}'.format(str(i), fname), 'w+') as f:
            for line in run:
                f.write(str(line[0])+','+str(line[1])+'\n')
            f.close()
    
