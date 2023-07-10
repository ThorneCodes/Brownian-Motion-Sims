# author: Gabriel Castillo Rosales

# imports
import numpy as np
import matplotlib.pyplot as plt

#funcionts

def plot(x, save=True,fname="NaN"):
    plt.cla()
    plt.scatter(np.linspace(0, x.size, num=x.size), x)
    if save:
        plt.savefig("../Data/Plots/{}.png".format(fname))
        plt.clf()
    else:
        plt.show()
        plt.clf()

def genData(pulls, size, plot=False, csv=True, test=False):
    np.random.seed(None)
    rng = np.random.default_rng()
    fnames = []
    for i in range(1, pulls+1):
        y = rng.random((int(size),))
        fname = "pull_{}_size_{}".format(str(i), str(size))
        fnames.append(fname)
        if csv:
            if test:
                np.savetxt("../Data/DF/Test/{}.csv".format(fname), y, delimiter=",")
            else:
                np.savetxt("../Data/DF/{}.csv".format(fname), y, delimiter=",")
        if plot:
            plot(y, fname)
    return fnames
