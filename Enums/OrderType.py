
from enum import Enum


class OrderType(Enum):
    Submission = 1
    Cancellation = 2
    Deletion = 3
    Visible_Execution = 4
    Hidden_Execution = 5
    Trading_Halt = 7

