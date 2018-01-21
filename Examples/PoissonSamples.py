
import numpy as np
import matplotlib.pyplot as plt


# http://eprints.lse.ac.uk/51370/1/Dassios_exact_simulation_hawkes.pdf

def intensity_path(lambda_, mu, alpha, beta, time):
    """
    :param lambda_: initial intensity value
    :param mu: long term mean
    :param alpha: scale
    :param beta: speed of mean reversion
    :param size: sample size
    :return: paths
    """
    t = 0
    _lambda_T_K = lambda_
    output = []
    jump_time = []

    while t < time:

        u = np.random.uniform()
        u_ = np.random.uniform()
        D = 1+(beta*np.log(u)/(_lambda_T_K-mu))
        s = (-1.0/beta) * np.log(D)
        s_ = (-1.0/mu) * np.log(u_)

        if D > 0:
            S = s * s_
        else:
            S = s_

        T = t + S
        jump_time.append(T)
        _lambda_T_K_1 = (_lambda_T_K - mu)*np.exp(-beta*(T-t)) + mu
        lambda_T_K_1 = _lambda_T_K_1 + alpha
        output.append(lambda_T_K_1)
        _lambda_T_K = lambda_T_K_1
        t = T

    return [output, jump_time]

def hawkes_process_sim_1():
    dt = 0.10
    _lambda_0 = 1.2
    alpha = 0.6
    beta = 0.8
    times = []
    events = []
    intensity = []

    time = 0
    s = 0
    T = 10
    times.append(0)
    events.append(0)
    intensity.append(_lambda_0)
    max_lambda = []
    while s < T:  # in the slides we keep going until s > T (we specify T)
        s += -(1.0 / _lambda_0) * np.log(np.random.rand())
        max_lambda.append(_lambda_0)
        while time < s:
            _lambda = _lambda_0 + alpha * np.exp(-beta * (s - time))
            intensity.append(_lambda)
            time += dt

        _lambda_0 = _lambda

    plt.plot(intensity)
    plt.show()

    None


def hawkes_process_sim_2(Time=5):
    _lambda = 1.2
    alpha = 0.6
    beta = 0.8
    s = 0.0
    t = 0.0
    dt = 0.01
    times = []
    path = list([])

    # first event
    while s <= Time:
        s += (-1.0/_lambda)*np.log(np.random.rand()) # event arrival
        times.append(s)
        while t <= s:
            path.append(_lambda + alpha*np.exp(-beta*t))
        
    plt.plot(path)
    plt.show()

    None


def concatenate(x, y):

    len_x = len(x)
    len_y = len(y)

    output = np.zeros(len_x+len_y)

    for i in range(0, len_x):
        output[i] = x[i]

    for i in range(0, len_y):
        output[len_x + i] = y[i]

    return output


if __name__ == '__main__':

    #times = hawkes_process_sim_2(5)

    first_event = 1.3077903913423528
    second_event = 2.1570675941251265
    steps = 100
    x1 = np.linspace(0.0, first_event, steps)
    x2 = np.linspace(first_event, second_event, steps)
    x3 = np.linspace(second_event, 5.0, steps)
    y1 = 1.20 + 0.60*np.exp(-0.80*x1)
    y2 = 1.80 + 0.60*np.exp(-0.80*x2)
    y3 = 1.80 + 0.60*np.exp(-0.80*x3)

    x = concatenate(concatenate(x1, x2), x3)
    y = concatenate(concatenate(y1, y2), y3)

    plt.plot(x, y)
    plt.show()

    """
    plt.subplot(2, 1, 1)
    plt.plot(path)
    plt.title('Intensity Path')

    plt.subplot(2, 1, 2)
    plt.plot(jump_time)
    plt.title('Jump Times')
    plt.show()
    """