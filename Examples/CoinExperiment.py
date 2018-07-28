
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def coin_experiment():
    experiments = 5
    length = 10
    u = np.random.uniform(0, 1, length)
    theta_1 = 0.60
    theta_2 = 0.50

    coin_1 = []
    coin_2 = []

    for i in range(0, experiments):
        x = np.random.sample()

        if x <= 0.5:  # select coin 1
            cont = np.random.uniform(0, 1, length)
            cont_experiment = []
            for j in range(0, length):
                if cont[j] <= theta_1:
                    cont_experiment.append(1)
                else:
                    cont_experiment.append(0)
            coin_1.append(cont_experiment)
        else:  # select coin 2
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


def kelly_criterion_wiki_example():

    current_toss = 0
    max_tosses = 300
    balance = 25
    prob_heads = 0.60
    stake = 0.20
    max_reward = 250
    reward_multiplier = 1.0

    while current_toss < max_tosses:
        reward = 0.0
        bet = stake*balance
        coin_outcome = np.random.uniform(0.0, 1.0, 1)
        if coin_outcome <= prob_heads:
            reward = reward_multiplier*bet
        else:
            reward = -bet
        balance += reward
        if balance >= max_reward:
            print('Final balance: {0}'.format(balance))
            print('Tosses: {0}'.format(current_toss))
            return
        current_toss += 1

    print('Final balance: {0}'.format(balance))

if __name__ == '__main__':
    #coin_experiment()
    kelly_criterion_wiki_example()
