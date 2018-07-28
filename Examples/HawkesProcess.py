
import numpy as np


def generate_path():
    l = 1.2
    alpha = 0.6
    beta = 0.8
    t = 0.0
    event = 0.7
    new_l = list()

    while t <= event:
        new_l.append(l + alpha*np.exp(-beta*(event-t)))
        t += 0.01
        
    pass


if __name__ == '__main__':
    generate_path()
