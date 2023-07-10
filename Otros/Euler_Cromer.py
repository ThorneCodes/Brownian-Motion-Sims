#Author: Gabriel Andrés Castillo Rosales

#impots
import numpy as np
import matplotlib.pyplot as plt
from sympy import *

# Functions

def plot(x, y, mode="plot"): #función para gráficar
    plt.clf()
    last = x[len(x)-1], y[len(y)-1]
    print(last)
    x, y = x[0:len(x)-1], y[0:len(x)-1]
    if mode == "plot":
        plt.plot(x, y)
        plt.scatter(last[0], last[1], color='red')
        plt.show()
    elif mode == "scatter":
        plt.scatter(x, y)
        plt.scatter(last[0], last[1], color='red', marker='x')
        plt.show()
    else:
        print("Invalid plot mode")

def bounceX(x_i): #Rebote básico para el eje x(cambia el signo de la coordenada x)
    if round(x_i, 10) > 1 or round(x_i, 10) < 0:
        return float(-1) # Hay colision
    else:
        return float(1) # NO hay colision
    
def bounceY(y_i): #Rebote básico para el eje y(cambia el signo de la coordenada y)
    if round(y_i, 10) > 1 or round(y_i, 10) < 0:
        return float(-1) # Hay colision
    else:
        return float(1) # NO hay colision

def floor_aux(a, y_0, y_1, t_i, h):
    m, g = 1, 9.78
    v = (y_1 - y_0)/h
    print("Value of speed at floor collision: ",v)
    fy_aux = lambda t: -1*v*(sin(a)).evalf() -g*t
    y_i = y_1 + h*fy_aux(t_i)
    return [y_i, -1*v]

def euler(s, a, h=0.0001): # Aplicación del método de Euler-Cromer

    # Inicialización
    a *= (pi/180).evalf()
    n = 10/h
    sx, sy = s, s
    dirX, dirY = 1, 1
    fx = lambda t: sx*(cos(a)).evalf()
    fy = lambda t: sy*(sin(a)).evalf() - 9.78*t
    T = np.linspace(0, 10+h, int(n))

    # Condiciones iniciales
    px, py = [0], [0]

    # Iteración
    for i in range(1, len(T)-1):
        x_i = px[i-1] + h*fx(T[i])
        y_i = py[i-1] + h*fy(T[i])

        if y_i < 0: # Revisa si hay rebote, puede causar problemas si el paso es muy pequeño
            temp = floor_aux(a, py[i-2], py[i-1], T[i], h)
            y_i, sy = temp[0], temp[1]
        else:
            if (x_i >= 1) and (y_i > 0.4 and y_i < 0.6): # Revisa si la particula salió de la caja y termina la iteración
                px.append(x_i)
                py.append(y_i)
                break
            else:
                sx, sy = sx*bounceX(x_i), sy*bounceY(y_i)
                x_i = px[i-1] + h*fx(T[i])
                y_i = py[i-1] + h*fy(T[i])

        px.append(x_i)
        py.append(y_i)
    
    return np.array([px, py])

# Ejemplo de uso
path = euler(6, 30)
plot(path[0], path[1])
