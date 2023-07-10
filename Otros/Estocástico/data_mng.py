#Author: Gabriel Castillo Rosales

#Imports
import numpy as np
import matplotlib.pyplot as plt

#Objects
class DataPool:

    def __init__(self, fname, test=True):
        self.seed = fname                                                       #it's not really a seed because the code uses an entropy state as seed for generating a dataset

        if test:
            self.data = np.genfromtxt('../Data/DF/Test/{}.csv'.format(fname), delimiter=',')        #All data in the pool - should be [[Data1], [Data2]]
        else:
            self.data = np.genfromtxt('../Data/DF/{}.csv'.format(fname), delimiter=',')
        self.out = None                                                         #What the output is - should be [[velocity],[angle]]

    def parse(self, ret=False):
        v_DF = self.data[0]
        a_DF = self.data[1]

        #Normalizing angle to [0, 2pi]
        a_DF_norm = np.array([float(i)/(2*np.pi) for i in a_DF])    #Puts every angle in terms of an angle in radians
        out = np.array([[v_DF[i], a_DF_norm[i]] for i in range(0, a_DF_norm.size-1)])

        #Deciding where to send the output
        if ret:
            self.out = out
        else:
            self.out = out
            return out

    def plot(self, save=False):
        plt.cla()
        # Polar plots in  2D
        v, a = self.out[0], self.out[1]
        fig, ax = plt.subplots(subplot_kw={'projection':'polar'})
        ax.plot(a, v)
        ax.set_rmax(np.amax(v))
        ax.set_rticks([i/15 for i in range(0, 15)]) # Sets the amount of radial ticks to 15
        ax.set_rlabel_position(-22.5) # Moves the radial label away from the line
        ax.grid(True) # Draws the grid
        ax.set_title('Randomly generated velocities on a polar axis')

        if save:
            plt.savefig('{}.csv'.format(fname))
            plt.clf()
        else:
            plt.show()
            plt.clf()

#Functions
