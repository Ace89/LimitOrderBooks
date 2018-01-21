
import numpy as np
import pandas as pd


def calc_sum_squares(centre, observations):
    output = 0.0

    for i in range(0,len(observations)):
        output += (centre - observations[i])**2

    return output


def get_state(ret, clusters):

    for i in range(0, len(clusters) + 1):

        if i==0:
            if ret < clusters[i]:
                return i
        elif i == len(clusters):
            if ret >= clusters[i-1]:
                return i
        else:
            if clusters[i-1] < ret <= clusters[i]:
                return i
    pass


def get_state_list(rets, clusters):
    state = []
    for i in range(0, len(rets)):
        state.append(get_state(rets[i], clusters))

    return state


def cluster_sum_squares(rets, clusters):
    counts = []
    filtered_rets = []
    cluster_ss=[]
    for i in range(0, len(clusters)+1):
        scen_count = []# add 1 if return falls in scenario
        scen_rets = []# add return if belongs to scenario to calc sum of squares
        for j in range(0, len(rets)):
            ret = rets[j]
            if i == 0:
                cluster = clusters[i]
                if ret < clusters[i]:
                    scen_count.append(1)
                    scen_rets.append(ret)
            elif i == len(clusters):
                cluster = clusters[i-1]
                if ret >= clusters[i-1]:
                    scen_count.append(1)
                    scen_rets.append(ret)
            else:
                cluster = 0.5*(clusters[i-1] + clusters[i])
                if clusters[i-1] < ret <= clusters[i]:
                    scen_count.append(1)
                    scen_rets.append(ret)
        counts.append(np.sum(scen_count))
        filtered_rets.append(scen_rets)
        cluster_ss.append(calc_sum_squares(cluster, scen_rets))

    return np.sum(cluster_ss)


def get_state_matrix(state, size):
    states = np.zeros((size, size))
    for i in range(1, len(state)):
        states[state[i-1], state[i]] += 1

    states_ = np.zeros((size,size))

    for i in range(0,size):
        denom = np.sum(states[i, :])
        for j in range(0,size):
            states_[i,j] = states[i, j] / denom

    return states_


def get_signal(state, state_matrix):
    # state_matrix -> [0, 1, 2, 3, 4]
    # state element of [0, 1, 2, 3, 4]

    row = state_matrix[state, :]
    up_move = 0.0
    down_move = 0.0

    for i in range(state, len(row)):
        up_move += row[i]

    for i in range(0, state):
        down_move += row[i]

    if up_move > down_move:
        return 'buy'
    else:
        return 'sell'


if __name__ == "__main__":

    """
    --- High   | Low     | Close
    --- 0.0388 | -0.0094 | 0.0313
    --- 0.0049 | -0.0050 | 0.0006
    --- 0.0143 | -0.0038 | 0.0106
    --- 0.0038 | -0.0148 | -0.0103
    --- 0.0053 | -0.0348 | -0.0280

    Daily log returns for the S&P 500 
    min daily log return = -14%
    max daily log return = 7.07% 
    
    calibrate transition matrix 
    """

    file_path = '~/Documents/Software Engineering/Dissertation/LimitOrderBooks/Data/'
    file_name = '^GSPC.csv'
    sp_data = pd.read_csv(file_path+file_name)

    close = sp_data['Close']
    high = sp_data['High']
    low = sp_data['Low']
    volume = sp_data['Volume']
    date = sp_data['Date']

    size_high = len(high)
    high_returns = []

    for i in range(1, size_high):
        high_returns.append(np.log(high[i]/high[i-1]))

    scen = [-0.03, -0.01, 0.01, 0.03]

    state = get_state_list(high_returns, scen)
    states = get_state_matrix(state, 5)
    state_ = get_state(high_returns[len(high_returns) - 1], scen)
    """
    print("method sum of squares: " + str(cluster_sum_squares(high_returns, scen)))
    print("Current buy or sell: " + str(get_signal(state_, states)))
    """
    window_length = 250
    window_cluster_ss = []
    window_buy_sell = []

    for i in range(window_length, len(high_returns)):
        ret_window = high_returns[i-window_length:i]
        window_state = get_state_list(ret_window, scen)
        window_state_matrix = get_state_matrix(window_state, len(scen)+1)
        window_state_ = get_state(ret_window[len(ret_window)-1], scen)
        window_cluster_ss.append(cluster_sum_squares(ret_window, scen))
        window_buy_sell.append(get_signal(window_state_, window_state_matrix))

    for i in range(0, 5):
        output = ""
        for j in range(0, 5):
            output += str(states[i, j]) + ", "
        print(output)