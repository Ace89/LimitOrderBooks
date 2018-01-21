"""
    Aim:
        Main method used to run program

    Git guide:
    http://rogerdudler.github.io/git-guide/

    Reading:
    https://stackoverflow.com/questions/419163/what-does-if-name-main-do
    https://stackoverflow.com/questions/2187583/whats-the-python-all-module-level-variable-for
    https://www.python-course.eu/python3_namespaces.php
    https://stackoverflow.com/questions/100210/what-is-the-standard-way-to-add-n-seconds-to-datetime-time-in-python
    http://parasec.net/transmission/order-book-visualisation/
    https://github.com/ab24v07/PyLOB
    https://github.com/danielktaylor/PyLimitBook
    https://www.r-bloggers.com/artificial-intelligence-in-trading-k-means-clustering/
    https://intelligenttradingtech.blogspot.co.uk/2010/06/quantitative-candlestick-pattern.html
    https://ibug.doc.ic.ac.uk/media/uploads/documents/expectation_maximization-1.pdf

    Notes:
    when using from import * only names listed in __all__ will be imported

"""

import timeit

import sample.TestScripts as test_scripts

__author__ = "Awais Talib"
__project__ = "Limit Order Books"
__maintainer__ = "Awais Talib"
__license__ = ""
__version__ = "0.1"
__all__ = ['unpack_orders', 'unpack_data']

start_time = timeit.default_timer()

if __name__ == "__main__":

    #test_scripts.ar_fit_test()
    #test_scripts.string_bucket_test()
    test_scripts.message_data_test()
    #test_scripts.data_bucket_structure_test()
    elapsed_time = timeit.default_timer()-start_time
    print("\nTime take to run the script: " + str(elapsed_time))
