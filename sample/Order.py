"""
    Aim:
        Outline Order class

        Order types
        1: Submission of a new limit order
        2: Cancellation (Partial deletion of a limit order) -> cannot exist on its own
        3: Deletion (Total deletion of a limit order) -> cannot exist on its own
        4: Execution of a visible limit order   -> cannot exist on its own
        5: Execution of a hidden limit order    -> cannot exist on its own their order id will be 0 in the data
        7: Trading halt indicator

        Execution type and Visibility are redundant at the moment
"""

from enum import Enum
from Enums.ExecutionType import ExecutionType
from Enums.OrderType import OrderType
from Enums.OrderDirection import OrderDirection
from Enums.Visibility import Visibility

__author__ = "Awais Talib"
__project__ = "Limit Order Books"
__maintainer__ = "Awais Talib"
__license__ = ""
__version__ = "0.1"
__all__ = ['unpack_orders', 'unpack_data']


class Order:

    def __init__(self, submission_time, direction, price, volume, visibility, order_type):
        self.submission_time = submission_time
        self.execution_time = []
        self.execution = []
        self.direction = direction
        self.price = price
        self.volume = volume
        self.visibility = visibility
        self.order_type = order_type

    def __hash__(self):
        return str(self.submission_time) + str(self.volume) + str(self.price)

    def cancel_order(self, time, volume):
        self.execution_time.append(time)
        self.execution.append(volume)
        self.execution.append(ExecutionType.Cancelled)

    def execute_order(self, time, volume):
        # what if order is executed multiple times i.e. order of 3000 executed in 1000 lots
        self.execution_time.append(time)
        self.execution.append(volume)
        self.execution.append(ExecutionType.Filled)
