#author: Gabriel Castillo Rosales

#Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import RNG
import sys

class container:

    def __init__(self, shape, aperture, dims):
        self.shape = shape.lower()
        self.apt = aperture

        if self.shape == "box":
            self.length = dims[0]
            self.heigth = dims[1]

            upper_wall, bottom_wall, left_wall, right_wall = [[float(self.length)*(i/1000), self.heigth] for i in range(0, 1000)],[[float(self.length)*(i/1000), 0] for i in range(0, 1000)],[[float(self.heigth)*(i/1000), self.length] for i in range(0, 1000)],[[float(self.heigth)*(i/1000), 0] for i in range(0, 1000)]
            self.walls = [upper_wall, bottom_wall, left_wall, right_wall]

            self.opening = [(self.heigth - aperture)/2, (self.heigth + aperture)/2] # opening is on Y axis
            
        elif self.shape == "circle":
            self.radius = dims
            self.walls = [[self.radius*np.sin(2*np.pi*(i/1000)), self.radius*np.cos(2*np.pi*(i/1000))] for i in range(0, 1000)]
            self.opening = aperture # Angle measured in radians
            
        elif self.shape == "3Dbox":
            self.length = dims[0]
            self.width = dims[1]
            self.heigth = dims[2]

            upper_plane = [[(i/1000)*self.length, (i*1000)*self.width, self.heigth] for i in range(0, 1000)]
            bottom_plane = [[(i/1000)*self.length, (i*1000)*self.width, 0] for i in range(0, 1000)]

            right_plane = [[(i/1000)*self.length, self.width, (i/1000)*self.heigth] for i in range(0, 1000)]
            left_plane = [[(i/1000)*self.length, 0, (i/1000)*self.heigth] for i in range(0, 1000)]

            back_plane = [[self.length, (i/1000)*self.width, (i/1000)*self.heigth] for i in range(0, 1000)]
            front_plane = [[0, (i/1000)*self.width, (i/1000)*self.heigth] for i in range(0, 1000)]

            self.walls = [upper_plane, bottom_plane, left_plane, right_plane, back_plane, front_plane]
            self.opening = [[(self.heigth - aperture)/2, (self.heigth + aperture)/2], [(self.width - aperture)/2, (self.width + aperture)/2]]
            # Opening is on the upper XY plane

    def update_opening(self, dx):
        if self.shape == "box":
            self.opening = [(self.heigth - (self.apt - dx))/2, (self.heigth + (self.apt - dx))/2]
        elif self.shape == "circle":
            self.opening = (self.apt - dx)
        elif self.shape == "3Dbox":
            self.opening = [[(self.heigth - (self.apt - dx))/2, (self.heigth + (self.apt - dx))/2], [(self.width - (self.apt - dx))/2, (self.width + (self.apt - dx))/2]]

    def isWall(self, pos):

        if self.shape == "box":
            if (pos[0] < self.length) and (pos[0] > 0):
                if (pos[1] < self.heigth) and (pos[1] > 0):
                    return False
                else:
                    return True
            else:
                return False
            
        elif self.shape == "circle":
            if pos >= self.radius:
                return True
            else:
                False
                
        elif self.shape == "3Dbox":
            if (pos[0] < self.length) and (pos[0] > 0):
                if (pos[1] < self.heigth) and (pos[1] > 0):
                    if (pos[2] < self.width) and (pos[2] > 0):
                        return False
                    else:
                        return True
                else:
                    return True
            else:
                return True

    def isExit(self, pos):

        if not self.isWall(pos):
            return False

        else:
            if self.shape == "box":
                if (pos[1] >= self.opening[0]) and (pos[1] <= self.opening[1]):
                    return True
                else:
                    return False
            elif self.shape == "circle":
                if abs(np.arcsin(pos[0]/self.radius)) <= self.opening/2:
                    return True
                else:
                    return False
            elif self.shape == "3Dbox":
                if (pos[1] >= self.opening[0][0]) and (pos[1] <= self.opening[0][1]):
                    if (pos[2] >= self.opening[1][0]) and (pos[2] <= self.opening[1][1]):
                        return True
                    else:
                        return False
                else:
                    return False
    
class particle: # For physic interactions between particles, like collisions between particles and for mass updating positions

    def __init__(self, p0, v0, mass, bm=True):
        self.mass = mass

        if type(p0) == type(np.array([0,0])):
            self.pos_array = p0
        elif type(p0) != type(np.array([0,0])):
            self.pos_array = np.array(p0)

        if type(v0) == type(np.array([0,0])):
            self.vel_array = v0
        elif type(v0) != type(np.array([0,0])):
            self.vel_array = np.array(v0)

        self.bm=bm


#update method is showing an array [1.0, 0] for [position, velocity] for some reason

    def update(self, dt, next_vel, ret=False, bm_pos=None, bm_vel=None, bm_mass=None): # dt is in seconds, tickrate is how many operations per second

        if self.bm == True:
            p1, v1 = [], next_vel
            for i in range(0, len(self.pos_array)):
                p0, v0 = self.pos_array[i], self.vel_array[i]
                p1.append(p0 + dt*v0)
            p1 = np.array(p1)
            if ret:
                self.pos_array, self.vel_array = p1, v1
                return p1
            else:
                self.pos_array, self.vel_array = p1, v1

        elif self.bm == False:
            p1, v1 = [], []
            p0, v0 = self.pos_array, self.vel_array

            for i in range(0, len(bm_pos)):
                bm_p0, bm_v0 = np.array(bm_pos[i]), np.array(bm_vel[i])

                if p0.all() == bm_p0.all():
                    v1 = (bm_mass/self.mass)*v0
                    p1 = p0 + dt*v1
                    self.pos_array, self.vel_array = p1, v1
                    break
                else:
                    continue

            if p0 not in bm_pos:
                p1 = p0 + dt*v0
                self.pos_array, self.vel_array = p1, v1
                
class sim:

    def __init__(self, name, n, shape, aperture, dims, bm_n=100, bm_m=0.001, t_max=60):
        self.name = name
        self.bm_n = bm_n
        self.dims = dims
        self.vel = None
        self.bm_particle_mass = bm_m
        self.timer = 0
        self.apt = aperture

        if shape == "box" or shape == "circle":
            self.repetitions = 2*n
            self.n_coords = 2
            self.test_particle = particle([0.5*self.dims[i] for i in range(0, len(self.dims))], [0,1], bm_m*50, bm=False)
        elif shape == "3Dbox":
            self.repetitions = 3*n
            self.n_coords = 3
            self.test_particle = particle([0.5*self.dims[i] for i in range(0, len(self.dims))], [0, 1, 0], bm_m*50, bm=False)

        self.container = container(shape, aperture, dims)

        self.bm_particles = RNG.genData(self.repetitions, bm_n) # List with the names of every file generated
        self.parse()
        self.genVel(init=True)

    def parse(self):
        final_len = len(self.bm_particles)/self.n_coords

        if self.n_coords == 2:
            i = 1
            while i < len(self.bm_particles):
                x_arr, y_arr = np.loadtxt("../Data/DF/pull_{}_size_{}.csv".format(str(i), self.bm_n)), np.loadtxt("../Data/DF/pull_{}_size_{}.csv".format(str(i+1), self.bm_n))
                out = []
                for j in range(0, len(x_arr)):
                    temp = [x_arr[j], y_arr[j]]
                    out.append(temp)
                i += 2
            self.bm_particles = np.array(out)
            np.savetxt("../Data/DF/{}.csv".format(self.name), out)

        elif self.n_coords == 3:
            i = 1
            while i < len(self.bm_particles):
                x, y, z = np.loadtxt("../Data/DF/pull_{}_size_{}.csv".format(str(i), self.bm_n)), "../Data/DF/{}.csv".format(str(i+1), self.bm_n), np.loadtxt("../Data/DF/pull_{}_size_{}.csv".format(str(i+2), self.bm_n))
                out = []
                for j in range(0, len(x)):
                    out.append([x[j], y[j], z[j]])
                i += 3
            self.bm_particles = np.array(out)
            np.savetxt("../Data/DF/{}.csv".format(self.name), out)

    def genVel(self, init=False):
        vel = []
        for i in range(0, len(self.bm_particles)):
            np.random.seed(None)
            rng = np.random.default_rng(i)
            temp = [rng.random()*(rng.integers(low=-1, high=1)) for j in range(0, self.n_coords)]
            vel.append(temp)
        if init:    
            self.vel = np.array(vel)
        else:
            return np.array(vel)

    def step(self, dt, plot=False, save=False):
        v1 = self.genVel()
        p0, v0, mass = self.bm_particles, self.vel, self.bm_particle_mass
        bm_particles_engine = particle(p0, v0, mass)    #Particles in brownian motion
        test_p0, test_v0, test_mass = self.test_particle.pos_array, self.test_particle.vel_array, self.test_particle.mass

        if plot:            
            p1 = bm_particles_engine.update(dt, v1, ret=True)
            self.container.update_opening(self.apt/dt)

            p1_x, p1_y = [p1[i][0] for i in range(0, len(p1))], [p1[i][1] for i in range(0, len(p1))]
            p0_x, p0_y = [p0[i][0] for i in range(0, len(p0))], [p0[i][1] for i in range(0, len(p0))]

            up_x, up_y = self.container.walls[0], [self.dims[2] for i in range(0, len(self.container.walls))]
            bot_x, bot_y = self.container.walls[1], np.array([0 for i in range(0, len(self.container.walls))])
            left_x, left_y = np.array([(self.dims[2]) for i in range(0, len(self.container.walls))]), self.container.walls[2]
            right_x, right_y = np.array([0 for i in range(0, len(self.container.walls))]), self.container.walls[3]

            plt.scatter(p0_x, p0_y)
            plt.scatter(p1_x, p1_y)
            plt.plot(up_x, up_y, color="black")
            plt.plot(bot_x, bot_y, color="black")
            plt.plot(left_x, left_y, color="black")
            plt.plot(right_x, right_y, color="black")
            plt.scatter(self.test_particle.pos_array[0], self.test_particle.pos_array[1])
            plt.savefig("../Data/Plots/plot_{}.png".format(str(self.name)+"_at_"+str(self.timer)))
            plt.clf()

            if save:
                np.savetxt("../Data/DF/{}.csv".format(str(self.name)+"_at_"+str(self.timer)), [self.bm_particles_engine.pos_array, self.test_particle.pos_array])

        else:
            bm_particles_engine.update(dt, v1)
            self.test_particle.update(dt, test_v0, bm_pos=bm_particles_engine.pos_array, bm_vel=bm_particles_engine.vel_array, bm_mass=bm_particles_engine.mass)
            self.container.update_opening(self.apt/dt)
            self.timer += dt
            if self.container.isWall(self.test_particle.pos_array):
                for i in range(0, len(self.test_particle.pos_array)):
                    if self.container.isExit(self.test_particle.pos_array):
                        if save:
                            np.savetxt("../Data/DF/{}.csv".format(str(self.name)+"_at_"+str(self.timer)), [self.bm_particles_engine.pos_array, self.test_particle.pos_array])
                        return [self.timer, True]
                    if self.test_particle.pos_array[i] == 0 or self.test_particle.pos_array[i] == self.dims[i]:
                        self.test_particle.vel_array[i] = -1*self.test_particle.vel_array[i]
                    else:
                        pass
                    if save:
                        np.savetxt("../Data/DF/{}.csv".format(str(self.name)+"_at_"+str(self.timer)), [self.bm_particles_engine.pos_array, self.test_particle.pos_array])
            else:
                if save:
                    np.savetxt("../Data/DF/{}.csv".format(str(self.name)+"_at_"+str(self.timer)), [self.bm_particles_engine.pos_array, self.test_particle.pos_array])
                return [self.timer, False]

Sim = sim("sim_test_0", 1000, "box", 0.5, [2,2])

Exit = False
maxTime = 60 #Measured in seconds
dt = 0

while (Sim.timer <= maxTime):
    step = Sim.step(0.1, save=True)
    Exit, time = step[1], step[0]

    if Exit == True:
        print("Exit time found at: {} seconds".format(time))
        break
    elif Exit == False and time >= maxTime:
        print("No exit found within 60 seconds")
    else:
        continue    
