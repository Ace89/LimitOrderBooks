"""
Bridge pattern example
"""

import abc
import numpy as np

import matplotlib.pyplot as plt

class Abstraction:

    def __init__(self, imp):
        self._imp = imp

    def operation(self):
        self._imp.operation_imp()


class Implementor(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def operation_imp(self):
        pass


class ConcreteImplementorA(Implementor):

    def operation_imp(self):
        print("Implementor A")


class ConcreteImplementorB(Implementor):

    def operation_imp(self):
        print("Implementor B")

if __name__ == '__main__':
    """
    concrete_implementor_a = ConcreteImplementorA()
    concrete_implementor_b = ConcreteImplementorB()
    abstraction = Abstraction(concrete_implementor_a)
    abstraction.operation()
    abstraction._imp = concrete_implementor_b
    abstraction.operation()
    """
    sims = 100000
    ts = np.zeros((sims,1))
    for i in range(1, sims):
        ts[i] = ts[i-1] + np.random.randn()

    lags = np.arange(2, 20)
    tau = [np.sqrt(np.std(np.subtract(ts[lag:], ts[:-lag]))) for lag in lags]

    plt.plot(np.log(lags), np.log(tau))
    plt.show()

    m = np.polyfit(np.log(lags), np.log(tau), 1)
    hurst = m[0]*2.0
    print("hurst: " + str(hurst))