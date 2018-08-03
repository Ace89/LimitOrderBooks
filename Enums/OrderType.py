
from enum import Enum


class OrderType(Enum):
    Submission = 1
    Cancellation = 2
    Deletion = 3
    VisibleExecution = 4
    HiddenExecution = 5
    Trading_Halt = 7

