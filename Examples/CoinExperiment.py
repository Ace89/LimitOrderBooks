
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':

    experiments = 5
    length = 10
    u = np.random.uniform(0, 1, length)
    theta_1 = 0.60
    theta_2 = 0.50

    coin_1 = []
    coin_2 = []

    for i in range(0, experiments):
        x = np.random.sample()

        if x <= 0.5: # select coin 1
            cont = np.random.uniform(0, 1, length)
            cont_experiment = []
            for j in range(0, length):
                if cont[j] <= theta_1:
                    cont_experiment.append(1)
                else:
                    cont_experiment.append(0)
            coin_1.append(cont_experiment)
        else: # select coin 2
            cont = np.random.uniform(0, 1, length)
            cont_experiment = []
            for j in range(0, length):
                if cont[j] <= theta_2:
                    cont_experiment.append(1)
                else:
                    cont_experiment.append(0)
            coin_2.append(cont_experiment)

    print('Coin 1')
    for exp in coin_1:
        exp_string = ''
        for vals in exp:
            exp_string += str(vals) + ','
        print(exp_string)

    print('Coin 2')

    for exp in coin_2:
        exp_string = ''
        for vals in exp:
            exp_string += str(vals) + ','
        print(exp_string)
