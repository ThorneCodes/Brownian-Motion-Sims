# Author: Gabriel Andrés Castillo Rosales

# Imports
import BM_v3 as BM


#functions

def __main__(runs, tpr, dt, n_p, n_s):

    r = 0
    print("Starting simulations")
    while r < runs:
        print("Simulation #{}".format(str(r)))
        box = BM.env(5,5,2,n_p, n_s=n_s)
        dot = BM.particle([box.X/2,0], [box.X/2, box.Y], 1)
        print("start up complete")
        print("running")
        while dot.timer <= tpr:
            box.update(2/tpr)
            dot.update(dt, box)
            BM.plot(box, dot, r, save=True)
        print("run complete")
        print("+-----------------------------------------------------------+")
        r += 1

__main__(25, 60, 0.1, 100, 100)
