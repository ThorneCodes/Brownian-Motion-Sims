#author: Gabriel Andrés Castillo Rosales

#imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import RNG, data_mng, time

#classes

class env:

    def __init__(self, length, width, aperture, n_p, n_s=100):
        self.X, self.Y, self.aperture = length, width, aperture

        plt.clf()
        self.left = [[0 for i in range(0, 50)], np.linspace(0, self.Y)]
        self.right = [[self.X for i in range(0, 50)],np.linspace(0, self.Y)]
        self.top = [np.linspace(0, self.X), [self.Y for i in range(0, 50)]]
        self.bot = [np.linspace(0, self.X), [0 for i in range(0, 50)]]
        self.apt = [np.linspace(float(self.X/2 - self.aperture/2), float(self.X/2 + self.aperture/2)), [self.Y for i in range(0, 50)]]
        self.vel = []
        
        self.fnames = RNG.genData(n_p, n_s, test=True)
        self.dots = []
        self.dot_p = 0
        for i in range(0, len(self.fnames)-1):
            temp_x, temp_y = np.genfromtxt("../Data/DF/Test/{}.csv".format(self.fnames[i])), np.genfromtxt("../Data/DF/Test/{}.csv".format(self.fnames[i+1]))
            self.dots.append([self.X*temp_x, self.Y*temp_y])

    def plot(self, save=False):
        plt.plot(self.left[0], self.left[1], color="black")
        plt.plot(self.right[0], self.right[1], color="black")
        plt.plot(self.top[0], self.top[1], color="black")
        plt.plot(self.bot[0], self.bot[1], color="black")
        plt.plot(self.apt[0], self.apt[1], color="red")

        plt.scatter(self.dots[self.dot_p][0], self.dots[self.dot_p][1], color="green")
        
        plt.grid()

        if save:
            plt.savefig("t0.png")
        else:
            plt.show()

    def update(self, dl):
        if self.dot_p < len(self.dots):
            self.dot_p += 1
        else:
            print("max time reached")
            quit()

        self.aperture += -1*dl
        self.apt = [np.linspace(float(self.X/2 - self.aperture/2), float(self.X/2 + self.aperture/2)), [self.Y for i in range(0, 50)]]    

class particle:

    def __init__(self, pos, vel, mass):
        self.timer = 0
        self.pos, self.vel, self.mass = pos, vel, mass
        self.p = [self.mass*self.vel[0], self.mass*self.vel[1]]

    def update(self, dt, container):
        self.timer += dt
        self.pos = np.array(self.pos) + dt*np.array(self.vel)

def plot(container, particle, number, save=False):

    box, dot = container, particle
    
    plt.plot(box.left[0], box.left[1], color="black")
    plt.plot(box.right[0], box.right[1], color="black")
    plt.plot(box.top[0], box.top[1], color="black")
    plt.plot(box.bot[0], box.bot[1], color="black")
    plt.plot(box.apt[0], box.apt[1], color="red")

    plt.scatter(box.dots[box.dot_p][0], box.dots[box.dot_p][1], color="green")
    plt.scatter(dot.pos[0], dot.pos[1], color="blue")
    plt.grid()

    plt.title("Sim #{} at {}[s]".format(number, dot.timer))
    
    if save:
        plt.savefig("C://Users/gabri/OneDrive/Documentos/Python Projects/SEP/Scripts/results/plots/Sim_{}_t_{}.png".format(number, dot.timer))
    else:
        plt.show()

##b = env(5,5,2,10)
##d = particle([b.X/2,0], [b.X/2, b.Y], 1)
##plot(b, d, 0)
