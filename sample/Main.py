"""
    Aim:
        Main method used to run program

"""

import timeit

import tests.TestScripts as test_scripts

__author__ = "Awais Talib"
__project__ = "Limit Order Books"
__maintainer__ = "Awais Talib"
__license__ = ""
__version__ = "0.1"
__all__ = ['unpack_orders', 'unpack_data']

start_time = timeit.default_timer()

if __name__ == '__main__':

    test_scripts.ar_fit_test()
    elapsed_time = timeit.default_timer()-start_time
    print("\nTime take to run the script: " + str(elapsed_time))
