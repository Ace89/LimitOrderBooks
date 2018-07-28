import numpy as np


def M_M_1_Simulation():
    # unit is minute
    # 20 buses arrive every hour
    arrival_rate = 20.0 / 60.0
    mu_rate = 25.0/60.0

    cumulative_state = 0

    sims = 1

    for i in range(0, sims):
        # system time
        t = 0.0
        t_end = 60.0
        state = 0
        t_1 = 0.0
        t_2 = t_end

        while t < t_end:
            if t_1 < t_2:   # arrival event
                t = t_1
                state = state + 1
                t_1 = t + np.random.exponential(1.0/arrival_rate)
                if state == 1:
                    t_2 = t + np.random.exponential(1.0/mu_rate)
            else:   # departure event
                t = t_2
                state = state - 1

                if state > 0:
                    t_2 = t + np.random.exponential(1.0/mu_rate)
                #else:
                #    t_2 = t_end
        cumulative_state += state
    print('Average state: ' + str(cumulative_state/sims))


def hawkes_process():
    import matplotlib.pyplot as plt
    mu = 1.2
    alpha = 0.6
    beta = 0.8
    t_end = 3.0
    intensity = mu
    t = -(1.0/intensity)*np.log(np.random.uniform(0, 1, 1))

    output = list()
    output.append(intensity)

    times = list()
    times.append(t)

    while t < t_end:
        t1 = t
        t = t - (1.0 / intensity) * np.log(np.random.uniform(0, 1, 1))
        intensity = mu + alpha*np.exp(-beta*(t-t1))
        intensity = intensity + alpha
        output.append(intensity)
        times.append(t)

    plt.scatter(times, output)
    plt.show()


if __name__ == '__main__':
    hawkes_process()
